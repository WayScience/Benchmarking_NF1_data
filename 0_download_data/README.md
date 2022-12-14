# Download NF1 Schwann Cell Images

In this module, we present the two datasets, one called pilot and a second dataset, that are downloaded to perform image-based cell profiling.

## NF1 Project Information

Information regarding the data for the NF1 project are as follows:

```
Assay: Modified Cell Painting

Channels: DAPI (DNA/Nuclei), GFP (Endoplasmic Reticulum), RFP (Cytoplasm) 

Cells: Schwann cells

Samples: Two genotypes of the NF1 gene, WT +/+ and Null -/-

Microscope: GE Deltavision Elite

Magnification: 20X

Bit-size: 16-bit

Number of images: 

- 96 images (Pilot dataset)

- 384 images (New dataset)

Total storage size: 

- 212.9 MB (Pilot dataset)

- 204.2 MB (New dataset - post conversion and cropping)
```

## Standard Metadata Name Structure

The standard metadata structure for this project is based on the pilot dataset.

![NF1 Pilot Data Metadata](example_images/NF1_Pilot_Data_Metadata.png "NF1 Pilot Data Metadata")

## Issue with new dataset

When comparing the pilot dataset and the second plate dataset (updated as of 12/09), there were three big differences between them:

1. Image composition
2. File naming (metadata)

Firstly, the images from the second plate were RGB (Figure 1).

![second_plate_dataset.png](example_images/second_plate_dataset.png)

The images from the pilot dataset are greyscale (which is the standard) and are 16-bit (Figure 2). 

![pilot_dataset.png](example_images/pilot_dataset.png)

Secondly, since the code within this project relies on the metadata structure from the pilot data (see above), the second plate would not be able to run properly.

## Solution

This led to the need to correct the second plate dataset to reflect standards from the pilot dataset. 
The corrections include using CellProfiler and Python.

In CellProfiler, we split the RGB images into three greyscale images (called red, green, and blue), taking the one of the three images that is connected to the channel (e.g. DAPI is the blue channel, GFP is green, RFP is red), and cropping the images to remove the scale.
The cropped images from each channel are saved as `.tif`files that are greyscale and 16-bit images.

Lastly, using Python, we created a function to reorder the file names and add metadata to fit the standards for analysis downstream.

---

## Steps to perform the conversion and correction of new dataset

### Step 1: Create conda environment

```sh
# Run this command to create the conda environment 
conda env create -f 0.download_NF1_data.yml
```

### Step 2: Activate conda environment

```sh
# Run this command to create the conda environment 
conda activate download-NF1-data
```

### Step 3: Execute preprocessing NF1 data

```sh
# Run this script in terminal
bash 1.preprocessing_data.sh
```
