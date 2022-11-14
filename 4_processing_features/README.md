# 4. Processing Extracted Single Cell Features 

In this module, we present our pipeline for processing outputted `.sqlite` file with single cell features from CellProfiler.
The processed features are saved into compressed `.csv.gz` for use during statistical analysis.

## Pycytominer

We use [Pycytominer](https://github.com/cytomining/pycytominer) to perform the aggregation, merging, and normalization of the NF1 single cell features.

For more information regarding the functions that we used, please see [the documentation](https://pycytominer.readthedocs.io/en/latest/pycytominer.cyto_utils.html#pycytominer.cyto_utils.cells.SingleCells.merge_single_cells) from the Pycytominer team.

### Normalization

Normalization of the data is important because there will be variety in the shapes of distributions. To make statsitical analysis easier, we normalize using standardized method.

---

## Step 1: Setup Processing Feature Environment

### Step 1a: Create Environment

Make sure you are in the `4_processing_features` directory before performing the below command.

```sh
# Run this command in terminal to create the conda environment for feature extraction
conda env create -f 4.processing_features.yml
```
