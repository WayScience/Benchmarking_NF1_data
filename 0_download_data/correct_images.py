#!/usr/bin/env python
# coding: utf-8

# # Correct Second Plate NF1 Images

# In[1]:


import pathlib
import importlib
correct = importlib.import_module("correctionutils")


# ## Correct Second Plate

# ### Set paths

# In[2]:


path_to_pipeline = "/home/jenna/NF1_SchwannCell_data/0_download_data/convert_crop_NF1_images.cppipe"
path_to_output = "/home/jenna/NF1_SchwannCell_data/0_download_data/NF1_Second_Plate_Corrected"
path_to_images = "/home/jenna/NF1_SchwannCell_data/0_download_data/NF1_Second_Plate"


# ### Run CellProfiler to convert and crop images and reformat the metadata

# In[3]:


correct.correct_images(path_to_pipeline, path_to_output, path_to_images)


# In[4]:


images_path = pathlib.Path(path_to_output)
output_folder_name = 'NF1_Second_Plate_Corrected'

correct.rename_images(images_path, output_folder_name)

