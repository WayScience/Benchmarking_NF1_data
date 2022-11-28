#!/bin/bash
jupyter nbconvert --to python extract_single_cell_features.ipynb
python extract_single_cell_features.py
