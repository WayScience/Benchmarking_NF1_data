#!/usr/bin/env python
# coding: utf-8

# # Illumination Correction of NF1 Images

# ## Import libraries

# In[1]:


import sys
import numpy as np
import matplotlib
import pathlib
from matplotlib import pyplot as plt
from pathlib import Path
import os
import skimage

# explicit import to PyBaSiC due to not having package support
sys.path.append("./PyBaSiC/")
import pybasic


# ## Helper functions to run PyBaSiC illumination correction
# - Allows for PyBaSiC to be run on any image sets and only need to input the path to the directory with the channel folders and the folder name of the channel that you
# want to work with.

# In[2]:


def load_pybasic_data(channel_path: pathlib.Path, channel: str, file_extension=".tif"):
    """
    Load all images from a specified directory in preparation for pybasic illum correction

    Parameters:
    channel_path (pathlib.Path): The directory where the channel folders are stored
    channel (str): The name of the channel (currently one of ["GFP", "RFP", "DAPI"])
    file_extension (str): The filename extension of the types of files to search for (default: ".tif")
    
    Returns:
        channel_images: list of ndarrays of the loaded in images
        image_files: list of strings of the paths to each image
    """
    # Creates a full pathlib.Path using the specified path to directory with channel folders and one of the channels that you designate
    full_channel_path = pathlib.Path(channel_path, channel)

    # For loop that iterates through the channel directory, coverts image paths to strings, finds strings with designated file extension (in this case the images are
    # of type .tif), strips the file extension from path, sorts the images to be in alphabetically order, and then loads in the data using the PyBaSiC function
    image_files = []
    for image_file in full_channel_path.iterdir():
        image_file = str(image_file)
        if image_file.endswith(file_extension):
            image_files.append(image_file.strip(file_extension))
   
    image_files.sort()
    channel_images = pybasic.tools.load_data(full_channel_path, file_extension, verbosity = True)

    return channel_images, image_files


def run_illum_correct(channel_path: pathlib.Path, channel: str, save_path: pathlib.Path, save_channel: str, output_calc: str = 'False'):
    """ calculates flatfield, darkfield, performs illumination correction on channel images., coverts to 8-bit and saves images into designated folder

    Parameters:
        channel_path (pathlib.Path): path to directory where image channels are located
        channel (str): name of channel
        save_path (pathlib.Path): path to directory where the corrected images will be saved to designated folders
        channel (str): name of channel with "_Corrected" (or however you want to designate the images) to create folder to save to
    """
    # Loads in the variables returned from "load_pybasic_data" function
    channel_images, image_files = load_pybasic_data(channel_path, channel)

    flatfield, darkfield = pybasic.basic(channel_images, darkfield=True)

    # Optional output that displays the plots for the flatfield and darkfield calculations if set to True (default is False)
    if output_calc == True:
        plt.title('Flatfield')
        plt.imshow(flatfield)
        plt.colorbar()
        plt.show()
        plt.title('Darkfield')
        plt.imshow(darkfield)
        plt.colorbar()
        plt.show()

    # Run PyBaSiC illumination correction function on loaded in images
    channel_images_corrected = pybasic.correct_illumination(
        images_list = channel_images, 
        flatfield = flatfield, 
        darkfield = darkfield,
        )
        
    # Covert illum corrected images to uint8 for downstream analysis
    corrected_images_coverted = np.array(channel_images_corrected)
    corrected_images_coverted[corrected_images_coverted<0] = 0 # makes the negatives 0
    corrected_images_coverted = corrected_images_coverted / np.max(corrected_images_coverted) # normalize the data to 0 - 1
    corrected_images_coverted = 255 * corrected_images_coverted # Scale by 255
    corrected_images = corrected_images_coverted.astype(np.uint8)

    # Save corrected images with suffix for identification
    new_channel_save_path = pathlib.Path(save_path, save_channel)
    
    for i, image in enumerate(corrected_images):
        orig_file = image_files[i]
        orig_file_name = orig_file.split("/")[4]
        new_filename = pathlib.Path(f'{new_channel_save_path}/{orig_file_name}_IllumCorrect.tif')

        # If the image has not been correcrted yet, then the function will save the image. If the image exists, it will skip saving.
        if not new_filename.is_file():
            skimage.io.imsave(new_filename, image)
        
        else:
            print(f"{new_filename.name} already exists!")


# ### Implementing helper functions to run illumination correction on each channel for NF1 data

# In[3]:


# Set location of input and output locations
# In this case, I am setting only one variable because my input and output directory is the same
channel_path = pathlib.Path('../PyBaSiC_Pipelines/NF1_Channels')

# Channels to process
channels = ["DAPI", "GFP", "RFP"]

# Perform illumination correction on all channels:
for channel in channels:
    print("Correcting", channel, "channel")
    # Folder to save the output channel
    save_channel = f"{channel}_Corrected"

# If you want to output the flatfield and darkfield calculations, then put "output_calc=True". If not, leave out from function since it is defaulted to False

# Perform illumination correction funtion for each channel
    run_illum_correct(
        channel_path=channel_path,
        channel=channel,
        save_path=channel_path,
        save_channel=save_channel
    )


# ## Process of PyBaSiC Illumination Correction
# **Note:** This section shows the process in which the helper functions are based on.
# 
# ### Create path and load in images
# The directory set up used for this experiment goes as such:
# ```
# 
# ├── NF1_SchwannCell_data/
# │   ├── 1_preprocessing_data/
# │   │   ├── PyBaSiC_Pipelines/
# │   │   │   ├── NF1_Channels/
# │   │   │   │   ├── DAPI/ or GFP/ or RFP/
# 
# ```

# In[4]:


channel_path = pathlib.Path('../PyBaSiC_Pipelines/NF1_Channels/DAPI')

# The for loop is running through the files within the folder designated by channel_path and will only take the names of the images and strips the ".tif"
# which leaves the image name that helps with identification of cells (genotype)

all_files = os.listdir(channel_path)
file_ext = ".tif"
image_files = []
for file in all_files:
    if file.endswith(file_ext):
        image_files.append(file.strip(file_ext))
image_files.sort()
channel_images = pybasic.tools.load_data(channel_path, '.tif', verbosity = True)


# ### Run PyBaSiC to calculate the flatfield and darkfield

# In[5]:


flatfield, darkfield = pybasic.basic(channel_images, darkfield=True)


# ### Displays the flatfield and darkfield that will be applied to the images

# In[6]:


# Based on documentation from the developers, it is recommended to manually check the flatfield function created using the functions below.
# If the flatfield looks smooth, then the correction will be done well.
# If it is noisey, then there is likely an issue with the correction.
# Source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5472168/

plt.title('Flatfield')
plt.imshow(flatfield)
plt.colorbar()
plt.show()
plt.title('Darkfield')
plt.imshow(darkfield)
plt.colorbar()
plt.show()


# ### Run illumination correction

# In[7]:


channel_images_corrected = pybasic.correct_illumination(
    images_list = channel_images, 
    flatfield = flatfield, 
    darkfield = darkfield,
)


# ### Conversion of Corrected Images

# In[8]:


# The default output for the corrected images was not compatable with downstream processes which required code to convert the images to `8-bit`. This code was
# utlized from Mitocheck Data Project - Preprocessing Training Data {https://github.com/WayScience/mitocheck_data/blob/main/1.preprocess_data/preprocess_training_data.ipynb}

corrected_images_coverted = np.array(channel_images_corrected)
corrected_images_coverted[corrected_images_coverted<0] = 0 # makes the negatives 0
corrected_images_coverted = corrected_images_coverted / np.max(corrected_images_coverted) # normalize the data to 0 - 1
corrected_images_coverted = 255 * corrected_images_coverted # Scale by 255
corrected_images = corrected_images_coverted.astype(np.uint8)


# ### Use `for` loop that adds suffix to corrected images and downloads them

# In[9]:


# Recommended to add a suffix that will indicate the which type of image it is, especially if the raw and corrected images look the same to the naked eye.

for i, image in enumerate(corrected_images):
    orig_file = image_files[i]
    new_filename = f'../PyBaSiC_Pipelines/NF1_Channels/DAPI_Corrected/{orig_file}_IllumCorrect.tif'
    skimage.io.imsave(new_filename, image)

