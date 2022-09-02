# NF1 Schwann Cell Data Project

## Data

The data used in this project is a modified Cell Painting assay on [schwann cells](https://www.ncbi.nlm.nih.gov/books/NBK544316/) from patients with [Neurofibromatosis type 1 (NF1)](https://medlineplus.gov/genetics/condition/neurofibromatosis-type-1/). 
In this modified Cell Painting, there are three channels:

- `DAPI` (Nuclei)
- `GFP` (Endoplasmic Reticulum)
- `RFP` (Actin)

There are two genotypes of the NF1 gene in these cells:

- Wild type (`WT`): In column 6 from the plate (e.g C6, D6, etc.)
- Heterozygous (`Het`): In column 7 from the plate (e.g C7, D7, etc.)

## Goal

The goal of this project is to predict NF1 genotype from schwann cell morphology. 
This can be done by using cell image analysis and representation learning to discover a biomarker from a pilot dataset that can be used for making predictions in future datasets. 
Once we discover a biomarker from these cells, we hope that our method can be used for drug discovery to treat this rare disease.

## Repository Structure

| Module | Purpose | Description |
| :---- | :----- | :---------- |
| [0_download_data](0_download_data/) | Download NF1 pilot data | Download 96 images of the NF1 pilot data  for analysis|
| [1_preprocessing_data](1_preprocessing_data/) | Perform Illumination Correction (IC) | Use `BaSiCPy` to perform IC on images per channel |
| [2_segmenting_data](2_segmenting_data/) | Segment Objects | Perform segmentation using `Cellpose` and outputing center (x,y) coordinates for each object |
| [3_extracting_features](3_extracting_features/) | Extract features | Use center (x,y) coordinates in `DeepProfiler` to extract features from all channels |
| [CellProfiler_pipelines](CellProfiler_pipelines/) | Perform a full pipeline on NF1 data using CellProfiler | Using `CellProfiler`, two pipelines are ran where one perform illumination correction and the second performs segmentation and feature extraction |
| TBD | TBD | TBD |