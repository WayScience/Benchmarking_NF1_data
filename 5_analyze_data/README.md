# 5. Analyzing NF1 features

In this module, we analyze the NF1 features for each plate using the various pipelines.
The analysis we perform include:

- UMAPS
- Correlation Heatmap
- Linear model
- Power analysis

## Jupyter Lab

For every module before this one, we have used [Visual Studio Code (vscode)](https://code.visualstudio.com/). 
Due to [an issue](https://github.com/microsoft/vscode-jupyter/issues/11374) with using R in Jupyter notebook for vscode, we are unable to use vscode to perform the analysis at this time.
To solve for this issue, we use Jupyter Lab as the IDE to perform the analysis notebooks. 

## Step 1: Create conda environment for R visualization

To create the conda environment used for visualization for R in Jupyter Lab, run the code block below:

```sh
conda env create -f visualize_env.yml
```

## Step 2: Create conda environment for analysis

To create the conda environment used for analysis notebooks (e.g. nf1_ks_test.ipynb), run the code block below:

```sh
conda env create -f 5.analyze_data.yml
```

## Step 3: Install Jupyter Lab

To install Jupyter Lab, follow [the instructions](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) found on their website.
In our case, we installed Jupyter Lab into `base` environment using the code block below:

```sh
conda install -c conda-forge jupyterlab
```

## Step 4: Start Jupyter Lab

To start Jupyter Lab, run the code block below:

```sh
jupyter lab
```

This will open Jupyter Lab into your browser. 
Using the file explorer, go to the "NF1_SchwannCell_data" directory, go into the "5_analyze_data" module, and start running the notebooks. 
You will need to change the pathing to the csv.gz outputs in the notebooks to the different pipelines to output the different figures.

