#!/bin/bash
jupyter nbconvert --to python *.ipynb

python extract_sc_features_cp_plate1.py
python extract_sc_features_dp_plate1.py
python extract_sc_features_cp_plate2.py
