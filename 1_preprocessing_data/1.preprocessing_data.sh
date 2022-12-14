#!/bin/bash
jupyter nbconvert --to python PyBaSiC_Pipelines/Illumination_Correction.ipynb
python PyBaSiC_Pipelines/Illumination_Correction.py
