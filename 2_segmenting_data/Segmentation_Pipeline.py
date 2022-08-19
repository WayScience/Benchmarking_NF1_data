#!/usr/bin/env python
# coding: utf-8

# # NF1 Data Segmentation
# 
# ## Finds the center (x,y) coordinates for the Schwann cells in the NF1 data

# ### Import libraries

# In[1]:


# from cellpose.io import logger_setup
from cellpose import models, core, io, utils

import pathlib
import pandas as pd
import skimage.io as io

import cv2
import numpy as np

import matplotlib.path as mplPath

import importlib

seg = importlib.import_module("segmentation_utils")


# ### Check if GPU is working for CellPose to work

# In[2]:


use_GPU = core.use_gpu()
print(">>> GPU activated? %d" % use_GPU)
# logger_setup()


# ### Segment NF1 Data

# In[3]:


# Set path to data to segment and path to save the information from segmentation to
data_path = pathlib.Path("../1_preprocessing_data/Corrected_Images/")
save_path = pathlib.Path("Segmented_Images")

# Model specs can be changed for each object that you are looking to segment.
# By using the CellPose GUI, you can find these parameters and prototype with them to assess the best specifications for your data
nuclei_model_specs = {
    "model_type": "cyto",
    "channels": [0, 0],
    "diameter": 50,
    "flow_threshold": 0.4,
    "remove_edge_masks": True,
}

cyto_model_specs = {
    "model_type": "cyto2",
    "channels": [1, 3],
    "diameter": 146,
    "flow_threshold": 0.4,
    "remove_edge_masks": True,
}

# Perform segmentation on objects
seg.segment_NF1(data_path, save_path, nuclei_model_specs, cyto_model_specs)

