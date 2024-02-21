#!/bin/csh

ipython --pdb doLinearRegressionVisualCell.py -- --label=realCC --images_filename=../../data/equalpower_C2_25hzPP.dat --responses_filename=../../data/030702.A.a03.C2_nsSumSpikes.dat --order=4 --nRDs=2
