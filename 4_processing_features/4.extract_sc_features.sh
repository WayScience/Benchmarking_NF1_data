#!/bin/bash
jupyter nbconvert --to python *.ipynb

python extract_sc_features_cp.py

python extract_sc_features_dp.py
