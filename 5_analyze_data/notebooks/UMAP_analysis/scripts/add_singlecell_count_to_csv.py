#!/usr/bin/env python
# coding: utf-8

# # Add single cell counts has metadata for NF1 data
# 
# - In this notebook, we add a metadata column for the number of single cells in a well into the normalized and feature selected data.

# ## Import libraries

# In[1]:


import pathlib
import pandas as pd

import sys
sys.path.append("../../")
import analysisutils as utils


# ## Set paths

# In[2]:


raw_data_path = pathlib.Path("../../../4_processing_features/data/nf1_sc_cellprofiler.csv.gz")
norm_data_path = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_cellprofiler.csv.gz")
norm_fs_data_path = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_cellprofiler.csv.gz")


# ## Read in `.csv` files
# 
# - The files loaded in include the raw data, normalized, and normalized with feature selection

# In[3]:


# Path to raw data
raw_data = pd.read_csv(raw_data_path, compression="gzip", index_col=0)
# need to reset index to remove "Metadata_WellRow" as the index
raw_data_ = raw_data.reset_index()

# Path to normalized data
norm_data = pd.read_csv(norm_data_path, compression="gzip", index_col=0)
# need to reset index to remove "Metadata_WellRow" as the index
norm_data = norm_data.reset_index()

norm_fs_data = pd.read_csv(norm_fs_data_path, compression="gzip", index_col=0)
# need to reset index to remove "Metadata_WellRow" as the index
norm_fs_data = norm_fs_data.reset_index()


# ## Find counts based on the well

# In[4]:


grouped_data = norm_data.groupby(["Metadata_WellRow", "Metadata_WellCol", "Metadata_Well"])['Metadata_WellRow'].count().reset_index(name='Metadata_number_of_singlecells')
grouped_data


# ## Assign number of single cells to respective well

# In[5]:


number_sc = []
for row in norm_data['Metadata_Well']:
    if row == 'C6' :    number_sc.append(12)
    elif row == 'C7':   number_sc.append(12)
    elif row == 'D6':   number_sc.append(5)
    elif row == 'D7':   number_sc.append(14)
    elif row == 'E6':   number_sc.append(9)
    elif row == 'E7':   number_sc.append(44)
    elif row == 'F6':   number_sc.append(7)
    elif row == 'F7':   number_sc.append(46)


# ## Insert the metadata for number of single cells into each `.csv`

# In[6]:


raw_data.insert(2, "Metadata_number_of_singlecells", number_sc)
norm_data.insert(2, "Metadata_number_of_singlecells", number_sc)
norm_fs_data.insert(2, "Metadata_number_of_singlecells", number_sc)


# ## Save `.csv` files with the new metadata column

# In[7]:


output_dir = pathlib.Path("../../../4_processing_features/data")

raw_output = pathlib.Path(f"{output_dir}/nf1_sc_cellprofiler.csv.gz")
norm_output = pathlib.Path(f"{output_dir}/nf1_sc_norm_cellprofiler.csv.gz")
norm_feature_select_output = pathlib.Path(f"{output_dir}/nf1_sc_norm_fs_cellprofiler.csv.gz")

raw_data.to_csv(raw_output)
norm_data.to_csv(norm_output)
norm_fs_data.to_csv(norm_feature_select_output)

