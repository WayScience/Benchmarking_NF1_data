#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts - Plate 2

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import cells, output


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../../../CellProfiler_pipelines"
output_dir = "../../data/Plate2/CellProfiler"


# ## Set paths to sqlite files

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file_pbcp = "NF1_data_pybasic_cp_plate2.sqlite"
single_cell_file_pbcp = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file_pbcp}"
platemap_file = f"{cp_dir}/Metadata/platemap_NF1_CP_Plate2.csv"

# Set path with name for outputted data
sc_output_file_pbcp = pathlib.Path(f"{output_dir}/nf1_sc_pybasic_cp_plate2.csv.gz")
sc_norm_output_file_pbcp = pathlib.Path(f"{output_dir}/nf1_sc_norm_pybasic_cp_plate2.csv.gz")
sc_norm_fs_output_file_pbcp = pathlib.Path(f"{output_dir}/nf1_sc_norm_fs_pybasic_cp_plate2.csv.gz")


# ## Set up names for linking columns between tables in the database file

# In[4]:


# Define custom linking columns between compartments
linking_cols = {
    "Per_Cytoplasm": {
        "Per_Cells": "Cytoplasm_Parent_Cells",
        "Per_Nuclei": "Cytoplasm_Parent_Nuclei",
    },
    "Per_Cells": {"Per_Cytoplasm": "Cells_Number_Object_Number"},
    "Per_Nuclei": {"Per_Cytoplasm": "Nuclei_Number_Object_Number"},
}


# ## Load and view platemap file

# In[5]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df.head()


# ## Set up `SingleCells` class from Pycytominer

# In[6]:


# Instantiate SingleCells class
sc_pbcp = cells.SingleCells(
    sql_file=single_cell_file_pbcp,
    compartments=["Per_Cells", "Per_Cytoplasm", "Per_Nuclei"],
    compartment_linking_cols=linking_cols,
    image_table_name="Per_Image",
    strata=["Image_Metadata_Well", "Image_Metadata_Plate"],
    merge_cols=["ImageNumber"],
    image_cols="ImageNumber",
    load_image_data=True
)


# ## Merge single cells 

# In[7]:


# Merge single cells across compartments
anno_kwargs = {"join_on": ["Metadata_well_position", "Image_Metadata_Well"]}

sc_df_pbcp = sc_pbcp.merge_single_cells(
    platemap=platemap_df,
    **anno_kwargs,
)

# Save level 2 data as a csv
output(sc_df_pbcp, sc_output_file_pbcp)

print(sc_df_pbcp.shape)
sc_df_pbcp.head()


# ## Normalize Data

# In[8]:


# Normalize single cell data and write to file
normalize_sc_df_pbcp = normalize(
    sc_df_pbcp,
    method="standardize"
)

output(normalize_sc_df_pbcp, sc_norm_output_file_pbcp)

print(normalize_sc_df_pbcp.shape)
normalize_sc_df_pbcp.head()


# ## Feature Selection

# In[9]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

feature_select_norm_sc_df_pbcp = feature_select(
    normalize_sc_df_pbcp,
    operation=feature_select_ops
)

output(feature_select_norm_sc_df_pbcp, sc_norm_fs_output_file_pbcp)

print(feature_select_norm_sc_df_pbcp.shape)
feature_select_norm_sc_df_pbcp.head()


# ---
# 
# ### Visualize basic count statistics

# In[10]:


sc_df_pbcp.Metadata_genotype.value_counts()


# In[11]:


pd.crosstab(sc_df_pbcp.Metadata_genotype, sc_df_pbcp.Metadata_Well)

