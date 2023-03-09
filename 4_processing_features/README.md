# 4. Processing Extracted Single Cell Features 

In this module, we present our pipeline for processing outputted `.sqlite` file with single cell features from [CellProfiler](https://cellprofiler.org/) (CP) and [DeepProfiler](https://github.com/cytomining/DeepProfiler) (DP).

The processed CP features are saved into compressed `.csv.gz` and DP features are saved as `.npz` files for use during statistical analysis.

We performed image-based analysis on 2 plates using a total of 3 pipelines (**note:** plate 2 has not been run through the DP method). The pipelines include:

1. CellProfiler for all parts of the process (e.g. IC, segmentation, and feature extraction)
2. PyBaSiC IC with CellProfiler segmentation and feature extraction
3. PyBaSiC IC, Cellpose segmentation (within CellProfiler), CellProfiler feature extraction
4. CellProfiler IC, Cellpose segmentation (within CellProfiler), CellProfiler feature extraction
5. PyBaSiC IC, Cellpose segmentation, and DeepProfiler feature extraction

| Illumination Correction | Segmentation | Feature Extraction |
| :---- | :----- | :---------- |
| CellProfiler | CellProfiler | CellProfiler |
| PyBaSiC | CellProfiler | CellProfiler |
| PyBaSiC | Cellpose | CellProfiler |
| CellProfiler | Cellpose | CellProfiler |
| PyBaSiC | Cellpose | DeepProfiler |

> Table 1. Detailing the software used for each part of the image-based analysis pipeline per method.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the merging, normalization, and feature selection of the NF1 single cell features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

### Normalization

CellProfiler and DeepProfiler features can display a variety of distributions across cells.
To facilitate analysis, we standardize all features (z-score) to the same scale.

### Feature selection

There are many features that are collected when using both CellProfiler and DeepProfiler. 
But, there are many features that are irrelevant due to the lack difference between single cells. 
Feature selection will only keep features that are more likely to show significance due to more variety in values.

---

## Step 1: Setup Processing Feature Environment

### Step 1a: Create Environment

Make sure you are in the `4_processing_features` directory before performing the below command.

```sh
# Run this command in terminal to create the conda environment
conda env create -f 4.processing_features.yml
```

## Step 2: Normalize and Feature Select Single Cell Features

There are a total of two plates currently using 5 different pipeline methods (except for plate 2 which does not use DeepProfiler at this time). 
There are currently a total of 3 notebooks:

1. [plate1_extract_sc_cp.ipynb](plate1_extract_sc_cp.ipynb): This notebook will run through all four methods that use CellProfiler as the feature extraction software for plate 1 data.
2. [plate2_extract_sc_cp.ipynb](plate2_extract_sc_cp.ipynb): This notebook will run through all four methods that use CellProfiler as the feature extraction software for plate 2 data.
3. [plate1_extract_sc_dp.ipynb](plate1_extract_sc_dp.ipynb): This notebook will run through the one method that uses DeepProfiler as the feature extraction software for plate 1 data.

Using the code below, you can run through all notebooks to extract all of the data for both plate 1 and plate 2.

**Note:** Make sure the `4.process-nf1-features` conda environment is activated.

```bash
# Run this script in terminal
bash extract_single_cells.sh
```
