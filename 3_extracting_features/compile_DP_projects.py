#!/usr/bin/env python
# coding: utf-8

# # Compile NF1 Projects for Nuclei and Cytoplasm - DeepProfiler

# ### Import Libraries

# In[1]:


import pathlib
import pandas as pd

import importlib
dp = importlib.import_module("DPutils")


# ### Define Project Paths

# In[2]:


# These paths are where all of the DeepProfiler folders and results will be located for each project
nuc_project_path = pathlib.Path('NF1_nuc_project-DP')
cyto_project_path = pathlib.Path('NF1_cyto_project-DP')


# ### Define Paths for `compile_project` Parameters

# In[3]:


checkpoint_name = 'efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5'
annotations_path = pathlib.Path('DP_files/NF1_annotations.csv')
images_load_path = pathlib.Path('../1_preprocessing_data/Corrected_Images/')
segmentation_data_path = pathlib.Path('../2_segmenting_data/Segmented_Images/')


# ### Compile Nucleus DeepProfiler Project

# In[4]:


object1 = "nuc"

dp.compile_project(nuc_project_path, checkpoint_name, annotations_path, images_load_path, segmentation_data_path, object1)


# ### Compile Cytoplasm DeepProfiler Project

# In[5]:


object2 = "cyto"

dp.compile_project(cyto_project_path, checkpoint_name, annotations_path, images_load_path, segmentation_data_path, object2)

