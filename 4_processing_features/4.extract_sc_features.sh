#!/bin/bash
jupyter nbconvert --to python extract_sc_features_cp.ipynb
python extract_sc_features_cp.py

jupyter nbconvert --to python extract_sc_features_dp.ipynb
python extract_sc_features_dp.py
