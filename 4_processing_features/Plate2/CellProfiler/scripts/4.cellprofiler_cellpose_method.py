#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts - CellProfiler IC and CellProfiler Cellpose plugin Method

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


# ## Set up paths to sqlite files and outputs

# ### CellProfiler IC with Cellpose plugin Method

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file_cpcellpose = "NF1_data_cellprofileric_cellpose_plate2.sqlite"
single_cell_file_cpcellpose = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file_cpcellpose}"
platemap_file = f"{cp_dir}/Metadata/platemap_NF1_CP.csv"

# Set path with name for outputted data
sc_output_file_cpcellpose = pathlib.Path(f"{output_dir}/nf1_sc_cellprofileric_cellpose.csv.gz")
sc_norm_output_file_cpcellpose = pathlib.Path(f"{output_dir}/nf1_sc_norm_cellprofileric_cellpose.csv.gz")
sc_norm_fs_output_file_cpcellpose = pathlib.Path(f"{output_dir}/nf1_sc_norm_fs_cellprofileric_cellpose.csv.gz")


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


# ## Load in platemap

# In[5]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df


# ## Set up `SingleCells` class from Pycytominer

# In[6]:


# Instantiate SingleCells class
sc_cpcellpose = cells.SingleCells(
    sql_file=single_cell_file_cpcellpose,
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

sc_df_cpcellpose = sc_cpcellpose.merge_single_cells(
    platemap=platemap_file,
    **anno_kwargs,
)

# Save level 2 data as a csv
output(sc_df_cpcellpose, sc_output_file_cpcellpose)

print(sc_df_cpcellpose.shape)
sc_df_cpcellpose.head()


# ## Normalize data

# In[8]:


# Normalize single cell data and write to file
normalize_sc_cpcellpose = normalize(
    sc_df_cpcellpose,
    method="standardize"
)

output(normalize_sc_cpcellpose, sc_norm_output_file_cpcellpose)

print(normalize_sc_cpcellpose.shape)
normalize_sc_cpcellpose.head()


# ## Feature Selection

# In[9]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

feature_select_norm_sc_cpcellpose = feature_select(
    normalize_sc_cpcellpose,
    operation=feature_select_ops
)

output(feature_select_norm_sc_cpcellpose, sc_norm_fs_output_file_cpcellpose)

print(feature_select_norm_sc_cpcellpose.shape)
feature_select_norm_sc_cpcellpose.head()


# ---
# 
# ### Visualize basic count statistics

# In[10]:


sc_df_cpcellpose.Metadata_genotype.value_counts()


# In[11]:


pd.crosstab(sc_df_cpcellpose.Metadata_genotype, sc_df_cpcellpose.Metadata_Well)

