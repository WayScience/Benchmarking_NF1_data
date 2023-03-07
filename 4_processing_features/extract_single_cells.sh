#!/bin/bash

# CellProfiler methods
jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts\
        --execute plate1_extract_sc_cp.ipynb

jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts\
        --execute plate2_extract_sc_cp.ipynb

# DeepProfiler methods
jupyter nbconvert --to python \
        --FilesWriter.build_directory=scripts\
        --execute plate1_extract_sc_dp.ipynb
