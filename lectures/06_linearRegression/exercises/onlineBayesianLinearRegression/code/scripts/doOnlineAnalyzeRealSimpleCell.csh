#!/bin/csh

ipython --pdb doOnlineBayesianLinearRegression.py -- --images_filename=https://www.gatsby.ucl.ac.uk/~rapela/neuroinformatics/2024/worksheets/linearRegression/data/equalpower_C2_25hzPP.dat --responses_filename=https://www.gatsby.ucl.ac.uk/~rapela/neuroinformatics/2024/worksheets/linearRegression/data/040909.a.c06.C2_nsSumSpikeRates.dat --update_delay=1e-10
