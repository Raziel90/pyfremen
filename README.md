# pyFreMEn
Fast Python implementation of the FreMEn model implemented in https://github.com/gestom/fremen

Frequency Map Enhancement (FreMEn) is a method that allows to introduce dynamics into spatial models used in the mobile robotics domain. Many of these models describe the environment by a set of discrete components with binary states. For example, cells of an occupancy grid are occupied or free, edges of a topological map are traversable or not, doors are opened or closed, rooms are vacant or occupied, landmarks are visible or occluded, etc. Typically, the state of every model component is uncertain, because it is measured indirectly by means of sensors which are affected by noise. The uncertainty is typically represented by means of a probability, that is normally considered a static variable. Thus, the probability of a particular component being in a particular state remains constant unless the state is being measured by the robot.

Frequency Map Enhancement considers the probability of each environment state as a function of time and represents it by a combination of harmonic components. The idea assumes that in populated environments, many of the observed changes are caused by humans performing their daily activities. Therefore, the environment's dynamics is naturally periodic and can be modelled by its frequency spectrum that represent a combination of harmonic functions that correspond to periodic processes influencing the environment. Such a model not only allows representation of environment dynamics over arbitrary timescales with constant memory requirements, but also prediction of future environment states. The proposed approach can be applied to many of the state-of-the-art environment models.

## Installation
The only necessary dependency is numpy
```bash
pip install numpy # if using pip
conda install numpy # if using conda
```

## Publications
----
1. T.Krajnik, J.P.Fentanes, G.Cielniak, C.Dondrup, T.Duckett: **[Spectral Analysis for Long-Term Robotic Mapping.]([https://link](http://labe.felk.cvut.cz/~tkrajnik/papers/fremen_2014_ICRA.pdf))** ICRA 2014. [bibtex](http://raw.githubusercontent.com/wiki/gestom/fremen/papers/fremen_2014_ICRA.bib) --> Original Paper
2. C.Coppola, T.Krajnik, T.Duckett, N.Bellotto: **[Learning temporal context for activity recognition](http://eprints.lincoln.ac.uk/23297/1/kaminka013.pdf)**, ECAI 2016. [bibtex](https://scholar.googleusercontent.com/scholar.bib?q=info:uKSiDo3lDHkJ:scholar.google.com/&output=citation&scisdr=CgXOPoTWEO285TfmUdc:AAGBfm0AAAAAX8HjSdfbXehm1MYf_RdUvFLQeYTOyGD2&scisig=AAGBfm0AAAAAX8HjSWcDLUa4fcjXvpeH_i6Ui7W3dEhQ&scisf=4&ct=citation&cd=-1&hl=en) --> Application on Activity Recognition
