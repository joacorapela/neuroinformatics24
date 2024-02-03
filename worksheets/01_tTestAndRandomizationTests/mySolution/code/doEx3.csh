#!/bin/csh

# usage: doZTest.py [-h] [--xbar XBAR] [--s S] [--n N] [--data_filename DATA_FILENAME] --mu0 MU0 --alpha ALPHA --test_type TEST_TYPE
ipython --pdb doZTest.py -- --xbar=79.7 --s=0.8 --n=100 --mu0=80 --alpha=0.05 --test_type=left-sided
