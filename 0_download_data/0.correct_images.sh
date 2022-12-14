#!/bin/bash
jupyter nbconvert --to python correct_images.ipynb
python correct_images.py
