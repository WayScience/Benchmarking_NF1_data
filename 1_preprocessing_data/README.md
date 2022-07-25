# 1. Preprocessing NF1 Data

In this module, we present our pipeline for preprocessing the NF1 Schwann Cell data.

## Illumination Correction

To correct for illumination issues within the NF1 data, we use the BaSiC method that was established in an article by [Peng et al.](https://doi.org/10.1038/ncomms14836).
We specifically use the Python implementation of this method, called [PyBaSiC](https://github.com/peng-lab/BaSiCPy).

## Step 1: Install PyBaSiC

Clone the repository into 1_preprocess_data/ with 

```console
git clone https://github.com/peng-lab/PyBaSiC.git
```

**Note:** This implementation does not have package support which means that it can not be imported as you normally would. 
To correct for this, use this line of code within your "Importing Libraries" cell to be able to use the functions with the 
[notebook](https://github.com/jenna-tomkinson/NF1_SchwannCell_data/blob/1.preprocessing_data/1_preprocessing_data/PyBaSiC_Pipelines/Illumination_Correction.ipynb).

```console
import sys
sys.path.append("./PyBaSiC/")
import pybasic
```