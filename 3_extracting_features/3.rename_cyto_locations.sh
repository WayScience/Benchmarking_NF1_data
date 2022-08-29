#!/bin/bash
jupyter nbconvert --to python rename_cyto_locations.ipynb
python rename_cyto_locations.py
