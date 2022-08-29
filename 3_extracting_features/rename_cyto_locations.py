#!/usr/bin/env python
# coding: utf-8

# # Rename Locations Files in the Cytoplasm DeepProfiler Project

# ### Import Libraries

# In[1]:


import pathlib
import importlib

dp = importlib.import_module("DPutils")


# ### Define Cytoplasm Locations Path

# In[2]:


# Currently, there is only one plate, so the directory is set to the plate and not the locations/ directory
cyto_locations_path = pathlib.Path("NF1_cyto_project-DP/inputs/locations/1/")


# ### Rename Files in `/inputs/locations` 

# In[3]:


dp.rename_cyto_locations(cyto_locations_path)

