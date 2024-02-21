#!/bin/csh

ipython --pdb doLinearRegressionVisualCell.py -- --label=simCC --images_filename=../../data/equalpower_C2_25hzPP.dat --responses_filename=../../results/ySimCC.dat --order=2 --nRDs=2
