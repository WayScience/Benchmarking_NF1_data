# 4. Processing Extracted Single Cell Features 

In this module, we present our pipeline for processing outputted `.sqlite` file with single cell features from CellProfiler (CP) and DeepProfiler (DP).

The processed CP features are saved into compressed `.csv.gz` and DP features are saved as `.npz` files for use during statistical analysis.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the merging, normalization, and feature selection of the NF1 single cell features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

### Normalization

CellProfiler and DeepProfiler features can display a variety of distributions across cells.
To facilitate analysis, we standardize all features (z-score) to the same scale.

---

## Step 1: Setup Processing Feature Environment

### Step 1a: Create Environment

Make sure you are in the `4_processing_features` directory before performing the below command.

```sh
# Run this command in terminal to create the conda environment
conda env create -f 4.processing_features.yml
```

## Step 2: Normalize and Feature Select Single Cell Features

### Step 2a: Set Up Paths

Within the [extract_sc_features_cp.ipynb](4_processing_features/extract_sc_features_cp.ipynb) notebook, you can change the paths to reflect the local paths or names for your machine (***IF* you changed anything from the original pipeline**) for the various parameters (e.g. CellProfiler directory, output directory, path to sqlite file, etc.)

As well, you can update the paths with the [extract_sc_features_dp.ipynb](4_processing_features/extract_sc_features_dp.ipynb) notebook if the paths to the project are different on your local machine.

### Step 2b: Run Extract Single Cell Features

Using the code below, run the notebook to extract and normalize single cell features from CellProfiler and DeepProfiler.

```bash
# Run this script in terminal
bash 4.extract_sc_features.sh
```
