#!/bin/bash

# run and convert notebooks for CellProfiler notebooks for each plate
jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts/ \ 
        --execute plate1_extract_sc_cp.ipynb

jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts/ \
        --execute plate2_extract_sc_cp.ipynb

# run and convert notebook for DeepProfiler for plate 1
jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts/ \
        --execute plate1_extract_sc_dp.ipynb
