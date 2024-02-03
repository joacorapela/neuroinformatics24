#!/bin/csh

# usage: doZTest.py [-h] [--xbar XBAR] [--s S] [--n N] [--data_filename DATA_FILENAME] --mu0 MU0 --alpha ALPHA --test_type TEST_TYPE
ipython --pdb doZTest.py -- --xbar=1.3 --s=2.6 --n=50 --mu0=2.0 --alpha=0.05 --test_type=two-sided
