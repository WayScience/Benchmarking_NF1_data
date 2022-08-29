# 2. Extract NF1 Features

In this module, I present the pipeline for extracting features from the NF1 data.

### Feature Extraction

To extract features from the NF1 data, I use [DeepProfiler](https://github.com/cytomining/DeepProfiler), commit [`8752f69`](https://github.com/cytomining/DeepProfiler/commit/8752f69686a0b0c53d4e829d598409506bac59f4).

Based off of previous projects in the lab, I decided to use a [pretrained model](https://github.com/broadinstitute/luad-cell-painting/tree/main/outputs/efn_pretrained/checkpoint) from the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting) with DeepProfiler.
DeepProfiler has the function to be able to train and create your own model (also named `checkpoint`) which I would like to test in the future.

The config files were made based off the one used in the [same repository from above](https://github.com/broadinstitute/luad-cell-painting).
The following changes were made to each config file, which are [NF1_nuc_config.json](DP_files/NF1_nuc_config.json) and [NF1_cyto_config.json](DP_files/NF1_cyto_config.json).

**Both:**
- `"Allele" -> "Genotype` In the LUAD study, alleles were compared across cell painting images. For the NF1 data, the genotypes of the NF1 gene are compared.
- `dataset: images: {file format: tif, bits: 16, width: 1080, height: 1080} -> dataset: images: {file format: tiff, bits: 8, width: 1224, height: 904}`: The image details are changed to reflect the NF1 data.
- `prepare: implement: true -> prepare: implement: false` We do not prepare the NF1 data with illumination correction (already done) or compression with Deep Profiler.
- `dataset: images: channels: [DNA, ER, RNA, AGP, Mito] -> dataset: images: channels: [DNA, ER, RNA]` While the Cell Painting dataset has multiple channels for cell images, the NF1 data only has the first three channels to examine.

**`NF1_nuc_config.json`:**
- `dataset: locations: box_size: 96 -> dataset: locations: box_size: 128` This change expands the size of the box put around each nuclei that DeepProfiler interprets. 
This expansion was recommended by Juan Caicedo to improve performance.

**`NF1_cyto_config.json`:**
- `dataset: locations: box_size: 96 -> dataset: locations: box_size: 256` This change expands the size of the box around each cell that DeepProfiler interprets. 
This expansion attempts to capture as much of the cytoplasm as possible (this will be benchmarked in the future to assess the best box size).

## Step 1: Setup Feature Extraction Environment

### Step 1a: Create Feature Extraction Environment

```sh
# Run this command to create the conda environment for feature extraction
conda env create -f 3.NF1_feature_extraction_env.yml
```

### Step 1b: Activate Feature Extraction Environment

```sh
# Run this command to activate the conda environment for Deep Profiler feature extraction

conda activate 3.feature-extraction-NF1
```

## Step 2: Install DeepProfiler

### Step 2a: Clone Repository

Clone the DeepProfiler repository into 3_extracting_features/ with 

```console
# Make sure you are located in 3_extracting_features/
cd 3_extracting_features/
git clone https://github.com/cytomining/DeepProfiler.git
```

### Step 2b: Install Repository

Install the DeepProfiler repository with

```console
# Make sure you are located in DeepProfiler/ to install
cd DeepProfiler/
pip install -e .
```

### Step 2c: Complete Tensorflow GPU Setup

Based on previous projects within the lab, we found using Tensorflow GPU when using DeepProfiler improves performance. To setup, follow [these instructions](https://www.tensorflow.org/install/pip#3_gpu_setup).
I use Tensorflow GPU while processing NF1 data.

## Step 3: Define Project Paths

Inside the notebook [compile_DP_projects.ipynb](compile_DP_projects.ipynb), the variables `nuc_project_path` and `cyto_project_path` need to be changed to reflect the desired object DeepProfiler project locations.

## Step 4: Compile DeepProfiler Project

In order to profile features with DeepProfiler, a project needs to be set up with a [certain file structure and files](https://github.com/cytomining/DeepProfiler/wiki/2.-Project-structure).

In [compile_DP_projects.ipynb](compile_DP_projects.ipynb), the necessary project structure is created using the functions from [DPutils.py](DPutils.py).

The config files ([NF1_nuc_config.json](DP_files/NF1_nuc_config.json)/[NF1_cyto_config.json](DP_files/NF1_cyto_config.json)) are copied to their corresponding projects and the pretrained model ([efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5](DP_files/efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5)) to both projects.
Both of these files are located within the [DP_files folder](DP_files/) for reference.

An `index.csv` file needs to be compiled as it necessary for DeepProfiler to load each image, which is created using the DP_files. Using the index.csv, the locations are compiled (in project/input/locations) and these csv files are necessary for DeepProfiler to find the single cells in each image.

For more information on DeepProfiler, please reference the [DeepProfiler wiki](https://github.com/cytomining/DeepProfiler/wiki/2.-Project-structure).

```bash
# Run this script to compile the DeepProfiler projects
bash 2.compile-DP-projects.sh
```

## Step 5: Extract Features with DeepProfiler

Change `path/to/DP_nuc_project` and `path/to/DP_cyto_project` below to the `nuc_project_path` and `cyto_project_path` set in step 3.
**Note:** Only include what is in the pathlib.Path(), not the full path for each variable (e.g pathlib.Path('NF1_nuc_project') -> use NF1_nuc_project)

```sh
# Run this script to extract features with DeepProfiler
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root `path/to/DP_nuc_project` --config NF1_nuc_config.json profile
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root `path/to/DP_cyto_project` --config NF1_cyto_config.json profile
```