#!/bin/bash
jupyter nbconvert --to python *.ipynb

python *.py
