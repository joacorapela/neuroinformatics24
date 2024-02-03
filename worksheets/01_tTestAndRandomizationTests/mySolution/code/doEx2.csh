#!/bin/csh

# usage: doZTest.py [-h] [--xbar XBAR] [--s S] [--n N] [--data_filename DATA_FILENAME] --mu0 MU0 --alpha ALPHA --test_type TEST_TYPE
ipython --pdb doZTest.py -- --xbar=2.4 --s=0.29 --n=35 --mu0=2.3 --alpha=0.05 --test_type=right-sided
