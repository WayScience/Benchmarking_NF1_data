#!/bin/bash
jupyter nbconvert --to python PyBaSiC_Pipelines/*.ipynb
python PyBaSiC_Pipelines/Illumination_Correction.py
