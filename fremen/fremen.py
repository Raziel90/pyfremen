from __future__ import print_function, division, absolute_import
import numpy as np

class Fremen:
    """
        Simple Fremen model implemented according to https://github.com/gestom/fremen 
        This model deconstructs a binary signal using the DFT algorithm in `num_periodicities` relevant periodicities.
        The period intervals used to decompose the signal are between max_period/num_periodicities and max_period / 1
        The model permits to reconstruct the signal using an arbitrary set of periodicities (up to num_periodicities) in the form of a probability function of the signal being high.
    """

    def __init__(self, num_periodicities=100, max_period = 7*24*3600, fremen_amplitude_th=0.0, default_orderi=3, periods_gt_duration=False):
        """
        This function initialises the model setting its hyperparameters.
        
        Args:
            num_periodicities (int, optional): maximum number of periodicities observed. Defaults to 100.
            max_period (int, optional): The maximum observed period length in seconds. Defaults to 7*24*3600.
            fremen_amplitude_th (float, optional): Amplitudes lower than this value are filtered out. Defaults to 0.0.
            default_orderi (int, optional): default order of the model used for estimations. Defaults to 3.
            periods_gt_duration (bool, optional): if True the periodicities larger than the observed interval are not considered. Defaults to False.
        """
        if (not isinstance(num_periodicities, int) or not num_periodicities > 0):
            raise ValueError('Input Error', "`num_periodicities` should be an integer >0. A good common value is 100")
        if (not isinstance(max_period, int) or not num_periodicities > 0):
            raise ValueError('Input Error', "`max_period` should be an integer >0. A good value could be the number of seconds in a week 7 * 24 * 3600. ")
        if (not isinstance(default_orderi, int) or not default_orderi > 0):
            raise ValueError('Input Error', "`default_orderi` should be an integer >0. A good value could 3. ")

        self._num_period = num_periodicities
        self._ampl_th = fremen_amplitude_th
        self._max_period = max_period
        self.default_orderi = default_orderi
        self.periods_gt_duration = periods_gt_duration
        
        self.gain = 0.5;
        self.firstTime = -1;
        self.lastTime = -1;
        self.measurements = 0;
        
        self.states = np.zeros(num_periodicities, dtype=complex)
        self.balances = np.zeros(num_periodicities, dtype=complex)
        self.amplitudes = np.zeros(num_periodicities)
        self.phases = np.zeros(num_periodicities)
        self.periods = np.zeros(num_periodicities)
        self.periods = max_period / np.arange(1, num_periodicities + 1)
        
    def __repr__(self):
        """
        Computes the string representation of the class. the representation includes the model orders up to `self.defaultorderi`
        """
        errs = 0
        orderi = self.default_orderi
        res_str = "Prior: {:.3f} Size: {}\n".format(self.gain, self.measurements)
        list_str = []
        for i in range(orderi):
            list_str.append('Frelement {} A:{:.3f} phi:{:.3f} T:{:.3f}'.format(i + 1, self.amplitudes[i], self.phases[i], self.periods[i])) 
        return res_str + "\n".join(list_str)
    
    def add(self, x, y):
        """adds the observations y made at time x to the model. This can be called multiple times to add further observations incrementally.

        Args:
            x (np.array(float)): input of the approximating function
            y (np.array(float)): observations of the approximating function made a time t 

        Returns:
            int : quantity of updated values
        """
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)

        if x.shape != y.shape or len(x.shape) > 1 or len(y.shape) > 1:
            raise ValueError('Observation Input Error', "The shapes of the observations vectors x,y should be the same and be monodimensional")
        elif x.shape[0] == 0:
            return 0
        
        if self.measurements == 0:
            self.firstTime = x[0]
            
        duration = x[-1] - self.firstTime
        firstIndex = (x <= self.lastTime).sum()
        numUpdated = x.shape[0] - firstIndex
        
        if numUpdated <= 0:
            return numUpdated
        
        self.lastTime = x[-1]
        
        oldGain, newGain = 0., 0.
        
        newGain = y[firstIndex:].sum()
        self.gain = (self.gain * self.measurements + newGain) / (self.measurements + x.shape[0])
        
        if oldGain > 0:
            self.balances *= self.gain / oldGain
        else:
            self.balances = np.complex(0)
                
        angles = x[firstIndex:] * 2 * np.pi / self.periods.reshape(-1, 1)
        self.states += (y[firstIndex:] * np.cos(angles) + 1j * y[firstIndex:] * np.sin(angles)).sum(axis=1)
        self.balances += (np.cos(angles) * self.gain + 1j * np.sin(angles) * self.gain).sum(axis=1)
            
        self.measurements += x.shape[0]
        temp = self.states - self.balances
        if self.periods_gt_duration:
            periods_in_duration = 1.5 * self.periods <= duration 
            self.amplitudes[periods_in_duration] = np.abs(temp)[periods_in_duration] / self.measurements
            self.amplitudes[~periods_in_duration] = 0.0
        else:
            self.amplitudes = np.abs(temp) / self.measurements
        self.amplitudes[self.amplitudes < 0.0] = 0.0
        self.phases = np.angle(temp)
        
        order = np.argsort(self.amplitudes)[::-1]

        self.states = self.states[order]
        self.balances = self.balances[order]
        self.amplitudes = self.amplitudes[order]
        self.phases = self.phases[order]
        self.periods = self.periods[order]
        return numUpdated
    
    def estimate(self, x, orderi, norm_ampl=False):
        """
        Reconstructs the signal using the static component + a set of `orderi` armonics.

        Args:
            x (np.array): input times of the reconstruction.
            orderi (int): order of the model.
            norm_ampl (bool, optional): if True the amplitude of the armonics is normalized to 1. Defaults to False.

        Returns:
            y_: the approximated values of the approximated function.
        """
        x = np.asarray(x)
        norm_ampl = self.amplitudes[:orderi] if not norm_ampl else self.amplitudes[:orderi]/2/(self.amplitudes[:orderi].sum())
        estimates = 2 * norm_ampl.reshape(-1, 1) * \
                     np.cos(x/self.periods[:orderi].reshape(-1, 1) * 2 * np.pi - self.phases[:orderi].reshape(-1, 1))
        probs = self.gain + estimates.sum(axis=0)
        probs[probs > 1.] = 1.
        probs[probs < 0.] = 0.
            
        return probs

        #estimates the state's entropy for the given times 
    def estimateEntropy(self, x, orderi, norm_ampl=False):
        """It estimates the entropy of the approximated function

        Args:
            x (np.array): input times for the calculation of the entropy.
            orderi (int): order of the model.
            norm_ampl (bool, optional): if True the amplitude of the armonics is normalized to 1. Defaults to False.

        Returns:
            np.ndarray(dtype=np.float64): array of the entropies for each input time.
        """
        x = np.asarray(x)
        entropy = np.zeros_like(x, dtype=np.float64)
        norm_ampl = self.amplitudes[:orderi] if not norm_ampl else self.amplitudes[:orderi]/2/(self.amplitudes[:orderi].sum())
        estimates = 2 * norm_ampl.reshape(-1, 1) * np.cos(x / self.periods[:orderi].reshape(-1, 1) * 2 * np.pi - self.phases[:orderi].reshape(-1, 1))
        estimates = self.gain + estimates.sum(axis=0)
        condition = (0. < estimates) & (estimates < 1.)
        entropy[condition] = -(estimates[condition] * np.log2(estimates[condition]) + (1 - estimates[condition]) * np.log2(1 - estimates[condition]))

        return entropy

        
    def evaluate(self, x, y, orderi, error_th=10.0, norm_ampl=False):
        """Evaluates the error of the predictions for the given times and measurements

        Args:
            x (np.array): input times for the calculation of the entropy.
            y ((np.array(dtype=np.int))): output of the function to compare to.
            orderi (int): order of the model.
            norm_ampl (bool, optional): if True the amplitude of the armonics is normalized to 1. Defaults to False.

        Returns:
            (np.array): (orderi+1x1) array containing the error between the constructed function and the signal
            (np.array): (orderi+1x1) the orders that surpass the error th 
        """
        x = np.asarray(x)
        y = np.asarray(y)
        estimate = 0.0
        time = 0.0
        state = 0.0
        estimates = np.zeros((orderi + 1, x.shape[0]))
        estimates[0, :] = self.gain
        evals = np.zeros(orderi + 1)
        norm_ampl = self.amplitudes[:orderi] if not norm_ampl else self.amplitudes[:orderi]/2/(self.amplitudes[:orderi].sum())
        estimates[1:, :] = (
            2 * norm_ampl.reshape(-1, 1) * \
            np.cos(x / self.periods[:orderi].reshape(-1, 1) * 2 * np.pi - self.phases[:orderi].reshape(-1, 1)))
            
        evals = np.abs(np.repeat(y.reshape(1, -1), orderi + 1, axis=0) - estimates).mean(axis=1)
        
        error = error_th
        
        index = np.where(evals < (error - 1e-3))
        
        return evals, index
