#!/usr/bin/env python
# coding: utf-8

# # Correct Second Plate NF1 Images

# In[1]:


import pathlib
import correctionutils as correct


# ## Correct Second Plate

# ### Set paths
# 
# **Paths are set as strings to use in command line for CellProfiler**

# In[2]:


path_to_pipeline = "convert_crop_NF1_images.cppipe"
path_to_output = "NF1_Corrected_Second_Plate"
path_to_images = "NF1_Second_Plate"


# ### Run CellProfiler to convert and crop images and reformat the metadata

# In[3]:


correct.correct_images(path_to_pipeline, path_to_output, path_to_images)


# In[4]:


images_path = pathlib.Path(path_to_output)
output_folder_name = path_to_output

correct.rename_images(images_path, output_folder_name)

