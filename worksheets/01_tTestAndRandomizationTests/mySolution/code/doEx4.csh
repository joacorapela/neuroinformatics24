#!/bin/csh

# usage: doTTest.py [-h] [--xbar XBAR] [--s S] [--n N] [--data_filename DATA_FILENAME] --mu0 MU0 --alpha ALPHA --test_type TEST_TYPE
ipython --pdb doTTest.py -- --data_filename=ex4Data.csv --mu0=100 --alpha=0.05 --test_type=left-sided
