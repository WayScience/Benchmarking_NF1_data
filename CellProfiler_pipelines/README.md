# CellProfiler Pipelines for NF1 Data Analysis

In this module, I present my CellProfiler (CP) pipelines used for illumination correction, segmentation, and feature extraction.

Since there are multiple methods are performing each of these steps, I decided to create two pipelines using [CellProfiler](https://cellprofiler.org/), version [4.2.4](https://cellprofiler-manual.s3.amazonaws.com/CellProfiler-4.2.4/index.html), a very commonly used and robust software for cell image analysis.
The goal of having multiple pipelines using various methods will allow for benchmarking for the "best" method later on. 

## Illumination Correction (IC) Pipeline

In the [NF1_illum.cpproj](Pipelines/NF1_illum.cpproj) CP project, I perform illumination correction on each channel (DAPI, GFP, RFP) of the NF1 data. 
There are three sets of `CorrectIlluminationCalculate` and `CorrectIlluminationApply` modules, where each set corrects a different channel and each contains different set of parameters as I have found using the same parameters for each channel does not always work.

For more information regarding these modules, you can reference my [Illumination Correction prototyping README](https://github.com/WayScience/CellProfiler_Prototyping/tree/main/1.illumination_correction) within the [CellProfiler_Prototyping repo](https://github.com/WayScience/CellProfiler_Prototyping). 
This README describes each of the parameters within these modules and provides further references.

Since the NF1 pilot data is small, this IC pipeline saves all of the images to use in the next pipeline.
For much larger datasets, it is standard to save the illumination correction function (which is much smaller and saves storage) and use that to perform IC in the next pipeline.

## Analysis Pipeline

In the [NF1_analysis.cpproj](Pipelines/NF1_analysis.cpproj) CP project, I perform segmentation and feature extraction.

### Segmentation

To perform segmentation in CP, the modules that were used were:

- **IdentifyPrimaryObjects:** Identify nuclei from the DAPI channel images. This creates a group for an object called `OrigNuclei`, which includes nuclei that are a part of cells that touch an edge of the image.

- **IdentifySecondaryObjects:** Identify whole cells using the nuclei from the previous module as a base from the RFP channel (stained for actin) images. 
These whole cells make up the object group called `Cells`.
Any cells that are touching at least one edge of the image will be removed along with its respective nucleus. 
This creates a new object group call `Nuclei`.

- **IdentifyTeritaryObjects:** Identify cytoplasm by subtracting out the "smaller identfied objects" (`OrigNuclei`) from the "larger identified objects" (`Cells`). 
`OrigNuclei` has to be used in this module over `Nuclei` due to an error downstream in the pipeline when using the latter object where it states "Cytoplasm is not in a 1:1 relationship with other objects".
This means that the number of cytoplasm is not the same as the other objects, which would be wrong because there should be the same amount of objects (e.g the number of cells should match the number of cytoplasm and nuclei).

Based on my understanding of CellProfiler, these modules identify the objects and create masks for each of them to use for feature extraction.

### Feature Extraction

Using the aforementioned object masks, each feature extraction module is applied to each image (from every channel).
This process measures various features for cells, cytoplasm, and nuclei in each of the three channels.
I followed the format of one of the CP pipelines from the [Broad Institute Platform Pipelines](https://github.com/broadinstitute/imaging-platform-pipelines/blob/master/cellpainting_UMUC9_20x_phenix_bin2/analysis_without_batchfile.cppipe).

The following modules were used and their respective parameters (not including selecting images and objects, which should be all images and the obejcts `Nuclei`, `Cytoplasm`, and `Cells`):

- **MeasureColocalization:**

    - "Set threshold as percentage of maximum intensity for the images": `Integer value`
    
    The default is set to `15.0`. 
    This sets a value to measure the correlation between intensities only for pixels that are above that threshold.

    - "Select where to measure correlation": `Within objects`, `Across entire image`, or `Both`

    The default is `Across entire image`, but I change it to `Within objects` as we are focused on the features from each of the single cells.

    - "Run all metrics?": `Yes` or `No`

    The default is `Yes`. When set to `No`, the user must choose the metrics they want. It is better to have all measurements run if you do not know what the various metrics are.

    - " Method for Costes thresholding": `Faster`, `Fast`, or `Accurate`

    The default is `Faster`. I use the default in this pipeline as it is what is used in the Broad Institute pipeline.

- **MeasureGranularity:**

    - "Measure within objects?" `Yes` or `No`

    The default is `No`. It is changed to `Yes` as we are extracting features from the objects.

    - "Subsampling factor for granularity measurement": `Integer value`

    The default is set to `0.25`. I kept the default value and did not follow the Borad Institute because the documentation states:

    >  Images are typically of higher resolution than is required for granularity measurements, so the default value is 0.25. 
    For low-resolution images, increase the subsampling fraction; for high-resolution images, decrease the subsampling fraction.

    Since I do not know if the NF1 images are more or less resolution than the ones the Broad Institute was using (as they increased the value to 0.5), I decided it was best to keep the default.

    - "Subsampling factor for background reduction": `Integer value`

    The default is set to `0.5`. Like above, I keep the default value as the documentation states:

    > The subsampling factor for background reduction is usually [0.125 – 0.25]. 
    This is highly empirical, but a small factor should be used if the structures of interest are large. 

    Since objects within the NF1 images are large, it makes sense to keep the default value.

    - "Radius of the structuring element": `Integer value`

    The default is set to `10`. 
    I kept the default and what the Broad Institute used as I am unsure how changing the value impacts the results.

    - "Radius of granular spectrum": `Integer value`

    The default is set to `16`. 
    I kept the default and what the Broad Institute used as I am unsure how changing the value impacts the results.

- **MeasureObjectIntensity:** 

    - No parameters in this module.

- **MeasureImageIntensity:**

    - "Measure the intensity only from areas enclosed by objects?": `Yes` or `No`
    
    The default is `No`. It is changed to `Yes` because the goal is it extract features from the objects/cells.

    - "Calculate custom percentiles": `Yes` or `No`

    The default is `No` and I keep this default value due to not knowing how this parameter would help the results.

- **MeasureObjectNeighbors:**

    - "Method to determine neighbors": `Within a specified distance`, `Adjacent`, or `Expand until adjacent`

    The default is `Expand until adjacent`. This default is not used in any module. 
    This parameter was chosen based on the example used from the Broad Institute.

    If `Within a specified distance`, another parameter is brought up:

    - "Neighbor distance": `Integer value`

    The default is set to `5`. 
    In one of the module, I increased it to 50 to try and make the measurement more accurate.

    - "Consider objects discarded for touching image border?": `Yes` or `No`

    The default is `Yes`. The default is kept because it is important to consider all the objects within an image. 
    Excluding them could yield wrong interpretation of the results. 
    
    For example, a specific genotype could have more cells clumped together than another genotype.
    If a lot of those neighbors are not included in the results because they are touching the edges, then you could not see this pattern.

    - "Retain the image of objects colored by numbers of neighbors?: `Yes` or `No`

    The default is `No`. 
    I keep the default in my pipeline.

    - Retain the image of objects colored by percent of touching pixels?"

    The default is `No`. 
    I keep the default in my pipeline.

**Note:** There are three of these modules used in this pipeline as shown in the Broad Institute pipeline. 
It only measures how many neighbors an object has. 
The three modules consist of one that measures `Nuclei` and two that measure `Cells` using different parameters.

- **MeasureObjectIntensityDistribution:**

    - "Calculate intensity Zernikes?": `None`, `Magnitudes only`, or `Magnitudes and phase`

    The default is `None`.
    I keep the default as it is done in the example pipeline.

    - "Object to use as center?": `These objects`, `Centers of other objects`, or `Edges of other objects`

    The default is `These objects` and is not changed.

    **Note:** You will need to add all of the objects (`Nuclei`, `Cytoplasm`, and `Cells`) in this module using the `Add another object` button.

    - "Scale the bins?": `Yes` or `No`

    The default is `Yes` and is not changed to match the example pipeline.

    - "Number of bins": `Integer value`

    The default is set to 4 and is not changed.

- **MeasureObjectSizeShape:**

    - "Calculate the Zernike features?": `Yes` or `No`

    The default is `Yes` and is not changed.

    - "Calculate the advanced features?": `Yes` or `No`

    The default is `No` and is not changed.

- **MeasureTexture:**

    - "Measure whole images or objects?": `Images`, `Objects` or `Both`

    The default is `Both`. I changed this parameter to `Objects` as this project focuses on the features coming from the objects and not the full images.

    - "Enter how many gray levels to measure the texture at": `Integer value`

    The default is `256` and is not changed.

    - "Texture scale to measure": `Integer value`

    The default is `3` and is not changed.

If want to know more about each of these parameters, you can use the `?` button on the far right of every parameter.
For further information on each of these modules, see the [Measurement section](https://cellprofiler-manual.s3.amazonaws.com/CellProfiler-4.2.1/modules/measurement.html) of the CellProfiler manual.

### Create SQLite Database File

The output of the entire pipeline (from IC to Analysis) is an SQLite file that will be used for preprocessing in the next module.
To get this SQLite file, I use the `ExportToDatabase` module.

The parameters that you need to change to get the file needed for the next step in the pipeline are:

- "Experiment Name": `String`

- "Name the SQLite database file": `String`

The default has it ending with `.db`, but for this experiment and for future steps, I have the file set as `.sqlite`.

- "Add a prefix to table names": `Yes` or `No`

The default is `Yes`. I do not see a need for the prefix so this parameter is set to `No`.

**Note:** All other `Yes` or `No` parameters are set to **`No`**.

- "Output file location": `Path`

This will be the directory where the file is saved to.

- "Export measurements for all objects to the database?": `All`, `None`, or `Select...`

The default is `All`. I have it set to `Select..` to make sure the measurements exported are for the objects `Nuclei`, `Cells`, and `Cytoplasm`.

- "Create one table per object, a single object table or a single object view": `One table per object type`, `Single object table`, or `Single object view`

The default is `Single object table`. 
The type of SQLite file wanted for this project is one that has a table for every object, I changed the parameter to `One table per object type`.

**Note:** Having `One table per object type` set as the parameter will cause a warning to pop up that says this parameter will cause the file outputted to not be used in CellProfiler Analyst (CPA) properly. 
Since we are not using CPA, this warning can be ignored.

## Step 1: Setup CellProfiler Environment

### Step 1a: Create Environment
 
 I used this [.yml file format](https://github.com/CellProfiler/CellProfiler/wiki/Conda-Installation) from the Wiki. 
 I updated the file and the Wiki page so that it would pip install the newest verison of CellProfiler instead of the older version that it had before.

 ```sh
# Run this command in terminal to create the conda environment for CellProfiler
conda env create -f download_cellprofiler.yml
```

### Step 1b: Activate Environment

```sh
# Run this command in terminal to activate the conda environment for CellProfiler
conda activate cp4
```

## Step 2: Open CellProfiler

```sh
# Run this command in terminal to start CellProfiler
cellprofiler
```

## Step 3: Run `illum.cpproj` and `analysis.cpproj`

`illum.cpproj` will be run first before running `analysis.cpproj`.
The same steps in order below will be followed for each project.

When CellProfiler is open, you will drag the CP project file from your file explorer into the box on the CellProfiler interface, as shown below:

![CellProfiler_fig1.png](Example_Images/CellProfiler_fig1.png)

After the project is loaded in, it will look like the image below:

![CellProfiler_pipeline.png](Example_Images/CellProfiler_pipeline.png)

Make sure that the `Images` module contains all of the NF1 images like the above image shows before proceeding.
Because I saved the pipeline with the images from the direcotry from my computer, the images will need to be deleted and readded into the `Images` module to reflect the correct path in your machine.

Before running the pipeline, change the "Output file location" in the `ExportToDatabase` module to the desired location for the SQLite file.

To run the illumination correction pipeline, press `Analyze Images` at the bottom right.

**Note:** If you do not want to see the pop ups from each module in the pipeline, you can turn the `eye symbol` off, like seen in the image above for all modules underneath `IdentifyTeritaryObjects`. 
This is done by just pressing that symbol to turn it on or off depending on what modules you want to view.
All of the segmentation modules are turned on as to see the how CellProfiler is segmenting each of the images as pipeline runs so you can stop the pipeline if you see something wrong in the segmentation.

### Runtime

I ran these pipelines on using a computer running Pop!_OS 20.04 LTS 64-bit with a AMD® Ryzen 7 3700x 8-core processor × 16 and NVIDIA graphics card.

It took 1 minute to run the `illum.cpproj` pipeline and 4 minutes to run the `analysis.cpproj`.