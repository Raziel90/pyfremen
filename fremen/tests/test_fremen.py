import unittest
import random

# import the fremen package
import fremen

# import the Fremen class
from fremen import Fremen

times = [0, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400, 54000,
         57600, 61200, 64800, 68400, 72000, 75600, 79200, 82800, 86400, 90000, 93600, 97200, 100800, 104400, 108000,
         111600, 115200, 118800, 122400, 126000, 129600, 133200, 136800, 140400, 144000, 147600, 151200, 154800, 158400,
         162000, 165600, 169200, 172800, 176400, 180000, 183600, 187200, 190800, 194400, 198000, 201600, 205200, 208800,
         212400, 216000, 219600, 223200, 226800, 230400, 234000, 237600, 241200, 244800, 248400, 252000, 255600, 259200,
         262800, 266400, 270000, 273600, 277200, 280800, 284400, 288000, 291600, 295200, 298800, 302400, 306000, 309600,
         313200, 316800, 320400, 324000, 327600, 331200, 334800, 338400, 342000, 345600, 349200, 352800, 356400, 360000,
         363600, 367200, 370800, 374400, 378000, 381600, 385200, 388800, 392400, 396000, 399600, 403200, 406800, 410400,
         414000, 417600, 421200, 424800, 428400, 432000, 435600, 439200, 442800, 446400, 450000, 453600, 457200, 460800,
         464400, 468000, 471600, 475200, 478800, 482400, 486000, 489600, 493200, 496800, 500400, 504000, 507600, 511200,
         514800, 518400, 522000, 525600, 529200, 532800, 536400, 540000, 543600, 547200, 550800, 554400, 558000, 561600,
         565200, 568800, 572400, 576000, 579600, 583200, 586800, 590400, 594000, 597600, 601200]

states = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
          1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1,
          1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class TestFremenInit(unittest.TestCase):
    def test_str_num_periodicities(self):
        with self.assertRaises(ValueError):
            s = Fremen(num_periodicities='osjdhgodsn')
    
    def test_str_orderi(self):
        with self.assertRaises(ValueError):
            s = Fremen(default_orderi='osjdhgodsn')


    def test_str_max_period(self):
        with self.assertRaises(ValueError):
            f = Fremen(max_period='osjdhgodsn')

    def test_order_repr(self):
        nper = 100
        o = random.randint(1, nper)
        f = Fremen(num_periodicities=nper, default_orderi=o)
        self.assertEqual(len(str(f).split('\n')), o + 1, "Lines in string representation don't match with the default order + 1")
        
class TestFremenModel(unittest.TestCase):

    def test_add_empty_x(self):
        f = Fremen()
        with self.assertRaises(ValueError):
            f.add([], [random.randint(0,1)for i in range(5)])

    def test_add_empty_y(self):
        f = Fremen()
        with self.assertRaises(ValueError):
            f.add([i for i in range(5)], [])

    def test_add_different_xy(self):
            f = Fremen()
            with self.assertRaises(ValueError):
                f.add([i for i in range(5)], [random.randint(0,1)for i in range(6)])

    def test_add_empty_xy(self):
            f = Fremen()
            up = f.add([], [])
            self.assertEqual(
                up,
                0, 'Adding empty observations should keep the model static.')
    
    def test_example_estimate_case(self):
            f = Fremen()
            f.add(times, states)
            self.assertLessEqual(
                f.estimate(times, orderi=4).sum() - 54.47299842276188,
                1e-15, "The test case provided had a wrong approximation!")

    def test_example_entropy_case(self):
            f = Fremen()
            f.add(times, states)
            self.assertLessEqual(
                f.estimateEntropy(times, orderi=11).sum() - 69.35590258966235,
                1e-15, "The test case provided had a wrong entropy estimation!")

    def test_example_evaluate(self):
            f = Fremen()
            f.add(times, states)
            self.assertLessEqual(
                f.evaluate(times, states, orderi=11)[0].sum() - 69.35590258966235,
                1e-15, "The test case provided had a wrong entropy estimation!")

    def test_example_cumulative(self):
            f1 = Fremen()
            f2 = Fremen()
            
            for i in range(0, len(times), 5):
                f1.add(times[i: min(i+6, len(times))], states[i: min(i+6, len(times))])
            f2.add(times, states)
            self.assertLessEqual(
                (f1.estimate(times, orderi=3) - f2.estimate(times, orderi=3)).sum(),
                1e-15, "In the test case provided building the model incrementally and one-shot provided different results.")

if __name__ == "__main__":
    unittest.main()
