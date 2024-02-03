#!/bin/csh

# usage: doTTest.py [-h] [--xbar XBAR] [--s S] [--n N] [--data_filename DATA_FILENAME] mu0 alpha test_type
ipython --pdb doTTest.py -- --data_filename=ex4Data.csv 100 0.05 left-sided
