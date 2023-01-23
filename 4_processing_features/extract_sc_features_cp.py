#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import cells, output


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../CellProfiler_pipelines"
output_dir = "data"


# ### Plate 1

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file = "NF1_data.sqlite"
single_cell_file = f"sqlite:///{cp_dir}/Analysis_Output/Plate1_Output/{sql_file}"
platemap_file = f"{cp_dir}/Metadata/platemap_NF1_CP.csv"

# Set path with name for outputted data
sc_output_file = pathlib.Path(f"{output_dir}/nf1_sc_cellprofiler.csv.gz")
sc_norm_output_file = pathlib.Path(f"{output_dir}/nf1_sc_norm_cellprofiler.csv.gz")
sc_norm_fs_output_file = pathlib.Path(f"{output_dir}/nf1_sc_norm_fs_cellprofiler.csv.gz")


# ### Plate 2

# In[4]:


# Set name and path of .sqlite file and path to metadata
sql_file2 = "NF1_data_plate2.sqlite"
single_cell_file2 = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file2}"
platemap_file2 = f"{cp_dir}/Metadata/platemap_NF1_CP_Plate2.csv"

# Set path with name for outputted data
sc_output_file2 = pathlib.Path(f"{output_dir}/nf1_sc_cellprofiler_plate2.csv.gz")
sc_norm_output_file2 = pathlib.Path(f"{output_dir}/nf1_sc_norm_cellprofiler_plate2.csv.gz")
sc_norm_fs_output_file2 = pathlib.Path(f"{output_dir}/nf1_sc_norm_fs_cellprofiler_plate2.csv.gz")


# ## Set up names for linking columns between tables in the database file

# In[5]:


# Define custom linking columns between compartments
linking_cols = {
    "Per_Cytoplasm": {
        "Per_Cells": "Cytoplasm_Parent_Cells",
        "Per_Nuclei": "Cytoplasm_Parent_OrigNuclei",
    },
    "Per_Cells": {"Per_Cytoplasm": "Cells_Number_Object_Number"},
    "Per_Nuclei": {"Per_Cytoplasm": "Nuclei_Number_Object_Number"},
}


# ## Plate 1

# ### Load and view platemap file

# In[6]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df


# ### Set up `SingleCells` class from Pycytominer

# In[7]:


# Instantiate SingleCells class
sc = cells.SingleCells(
    sql_file=single_cell_file,
    compartments=["Per_Cells", "Per_Cytoplasm", "Per_Nuclei"],
    compartment_linking_cols=linking_cols,
    image_table_name="Per_Image",
    strata=["Image_Metadata_Well", "Image_Metadata_Plate"],
    merge_cols=["ImageNumber"],
    image_cols="ImageNumber",
    load_image_data=True
)


# ### Merge single cells 

# In[8]:


# Merge single cells across compartments
anno_kwargs = {"join_on": ["Metadata_well_position", "Image_Metadata_Well"]}

sc_df = sc.merge_single_cells(
    platemap=platemap_df,
    **anno_kwargs,
)

# Save level 2 data as a csv
output(sc_df, sc_output_file)

print(sc_df.shape)
sc_df.head()


# ### Normalize Data

# In[9]:


# Normalize single cell data and write to file
normalize_sc_df = normalize(
    sc_df,
    method="standardize"
)

output(normalize_sc_df, sc_norm_output_file)

print(normalize_sc_df.shape)
normalize_sc_df.head()


# ### Feature Selection

# In[10]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

feature_select_norm_sc_df = feature_select(
    normalize_sc_df,
    operation=feature_select_ops
)

output(feature_select_norm_sc_df, sc_norm_fs_output_file)

print(feature_select_norm_sc_df.shape)
feature_select_norm_sc_df.head()


# ---
# 
# ### Visualize basic count statistics for Plate 1

# In[11]:


sc_df.Metadata_genotype.value_counts()


# In[12]:


pd.crosstab(sc_df.Metadata_genotype, sc_df.Metadata_Well)


# ---
# 
# ## Plate 2

# ### Load and view platemap file

# In[13]:


# Load platemap file
platemap_df2 = pd.read_csv(platemap_file2)
platemap_df2


# ### Set up `SingleCells` class from Pycytominer

# In[14]:


# Instantiate SingleCells class
sc2 = cells.SingleCells(
    sql_file=single_cell_file2,
    compartments=["Per_Cells", "Per_Cytoplasm", "Per_Nuclei"],
    compartment_linking_cols=linking_cols,
    image_table_name="Per_Image",
    strata=["Image_Metadata_Well", "Image_Metadata_Plate"],
    merge_cols=["ImageNumber"],
    image_cols="ImageNumber",
    load_image_data=True
)


# ### Merge single cells 

# In[15]:


# Merge single cells across compartments
anno_kwargs = {"join_on": ["Metadata_well_position", "Image_Metadata_Well"]}

sc_df2 = sc2.merge_single_cells(
    platemap=platemap_df2,
    **anno_kwargs,
)

# Save level 2 data as a csv
output(sc_df2, sc_output_file2)

print(sc_df2.shape)
sc_df2.head()


# ### Normalize data

# In[16]:


# Normalize single cell data and write to file
normalize_sc_df2 = normalize(
    sc_df2,
    method="standardize"
)

output(normalize_sc_df2, sc_norm_output_file2)

print(normalize_sc_df2.shape)
normalize_sc_df2.head()


# ### Feature selection

# In[17]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

feature_select_norm_sc_df2 = feature_select(
    normalize_sc_df2,
    operation=feature_select_ops
)

output(feature_select_norm_sc_df2, sc_norm_fs_output_file2)

print(feature_select_norm_sc_df2.shape)
feature_select_norm_sc_df2.head()


# ---
# 
# ### Visualize basic count statistics for Plate 2

# In[18]:


sc_df2.Metadata_genotype.value_counts()


# In[19]:


pd.crosstab(sc_df2.Metadata_genotype, sc_df2.Metadata_Well)

