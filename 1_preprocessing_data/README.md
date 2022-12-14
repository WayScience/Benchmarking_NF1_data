# 1. Preprocessing NF1 Data

In this module, we present our pipeline for preprocessing the NF1 Schwann Cell data.

## Illumination Correction (IC)

To correct for illumination issues within the NF1 data, we use the BaSiC method that was established in an article by [Peng et al.](https://doi.org/10.1038/ncomms14836).
We specifically use the Python implementation of this method, called [PyBaSiC](https://github.com/peng-lab/BaSiCPy).

Illumination correction is an important step in cell image analysis pipelines as it helps with downstream processes like segmentation (more accuracy in segmenting shape and identifying objects to segment) and feature extraction (accurate measurements in intensity, texture, etc.).

Visualizing if images need IC can be simple or difficult depending on the dataset. 
In the NF1 dataset, identifying illumination issues is impossible to capture with the human eye.

To visualize the illumination issues, we use Fiji to increase the maximum limits of the display range to brighten the images using the `B&C` tool (Figure 1).

![NF1_IC_Demonstration.png](example_figs/NF1_IC_Demonstration.png)
> Figure 1. Use of Fiji to determine illumination issues. This figure shows how increasing the maximum limit for the display range reveals illumination issues (e.g. vignetting like in the DAPI channel). Increasing upper limits shows brighter areas in the image that were hidden previously.

The documentation regarding this tool states:

> ImageJ displays images by linearly mapping pixel values in the display range to display values in the range 0-255. Pixels with a value less than the minimum are displayed as black and those with a value greater than the maximum are displayed as white. `Minimum` and `Maximum` control the lower and upper limits of the display range.

After running PyBaSiC and generating corrected images, we use Fiji to confirm that the illumination issues been corrected (Figure 2).

![NF1_IC_Brightened_Fig.png](example_figs/NF1_IC_Brightened_Fig.png)
> Figure 2. Visualizing IC through comparison. This figure shows the impact of IC using PyBaSiC on the raw images. 

Without using Fiji, the raw and corrected images look almost identical and it is very difficult to tell (with the human eye) if the illumination issues have been corrected. (Figure 3).

![NF1_IC_No_Brightening.png](example_figs/NF1_IC_No_Brightening.png)
> Figure 3. Raw versus corrected images. This figure shows how only looking at the images without any editing does not give any indication if the IC worked or not.

--- 

## Step 1: Install PyBaSiC

Clone the repository into 1_preprocess_data/ with 

```console
git clone https://github.com/peng-lab/PyBaSiC.git
```

**Note:** This implementation does not have package support which means that it can not be imported as you normally would. 
To correct for this, use this line of code within your "Importing Libraries" cell to be able to use the functions within the 
[notebook](PyBaSiC_Pipelines/Illumination_Correction.ipynb).

```console
import sys
sys.path.append("./PyBaSiC/")
import pybasic
```

## Step 2: Install Fiji

Follow the instructions on the [ImageJ website](https://imagej.net/software/fiji/downloads) to install Fiji.
We use the 64-bit Linux install.

## Step 3: Create Conda Environment

```sh
# Run this command to create the conda environment for NF1 segmentation
conda env create -f 1.preprocessing_data.yml
```

## Step 4: Activate Conda Environment

```sh
# Run this command to activate the conda environment for NF1 segmentation
conda activate preprocessing-nf1
```

## Step 5: Execute Preprocessing NF1 Data

```bash
# Run this script in terminal to segment NF1 data
bash 1.preprocessing_data.sh
```

