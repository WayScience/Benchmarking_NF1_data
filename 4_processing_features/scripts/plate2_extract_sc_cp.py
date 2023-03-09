#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for CellProfiler readouts - `Plate 2`

# ## Import Libraries

# In[1]:


import pandas as pd
import pathlib

import extraction_utils as sc_util


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = pathlib.Path("../CellProfiler_pipelines")
output_dir = pathlib.Path("data/Plate2/CellProfiler")


# ## Set up paths to sqlite files and outputs

# In[3]:


# Set paths for all cellprofiler method
method1 = "all_cellprofiler"
sql_file1 = f"{method1}.sqlite"
single_cell_file1 = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file1}"

# set paths for pybasic cellprofiler method
method2 = "pybasic_cellprofiler"
sql_file2 = f"{method2}.sqlite"
single_cell_file2 = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file2}"

# set paths for pybasic cellpose method
method3 = "pybasic_cellpose"
sql_file3 = f"{method3}.sqlite"
single_cell_file3 = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file3}"

# set paths for cellprofiler cellpose method
method4 = "cellprofiler_cellpose"
sql_file4 = f"{method4}.sqlite"
single_cell_file4 = f"sqlite:///{cp_dir}/Analysis_Output/Plate2_Output/{sql_file4}"

# set path to the platemap for plate 2
platemap_file = pathlib.Path(f"{cp_dir}/Metadata/platemap_NF1_CP_Plate2.csv")


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
platemap_df.head()


# ## Perform extraction with All CellProfiler method
# 
# - Merge single cells
# - Normalize
# - Feature selection on normalized features

# In[6]:


sc_util.extract_single_cells(
    single_cell_file=single_cell_file1,
    linking_cols=linking_cols,
    platemap_df=platemap_df,
    output_folder=output_dir,
    method_name=method1,
    norm_feature_select=True,
)


# ## Perform extraction with PyBaSiC CellProfiler method
# 
# - Merge single cells
# - Normalize
# - Feature selection on normalized features

# In[7]:


sc_util.extract_single_cells(
    single_cell_file=single_cell_file2,
    linking_cols=linking_cols,
    platemap_df=platemap_df,
    output_folder=output_dir,
    method_name=method2,
    norm_feature_select=True,
)


# ## Perform extraction with PyBaSiC Cellpose method
# 
# - Merge single cells
# - Normalize
# - Feature selection on normalized features

# In[8]:


sc_util.extract_single_cells(
    single_cell_file=single_cell_file3,
    linking_cols=linking_cols,
    platemap_df=platemap_df,
    output_folder=output_dir,
    method_name=method3,
    norm_feature_select=True,
)


# ## Perform extraction with CellProfiler Cellpose method
# 
# - Merge single cells
# - Normalize
# - Feature selection on normalized features

# In[9]:


sc_util.extract_single_cells(
    single_cell_file=single_cell_file4,
    linking_cols=linking_cols,
    platemap_df=platemap_df,
    output_folder=output_dir,
    method_name=method4,
    norm_feature_select=True,
)


# ---
# ## Visualize count statisitics

# ### All CellProfiler

# In[10]:


data_path = f"{output_dir}/nf1_sc_{method1}.csv.gz"
data_df = pd.read_csv(data_path, compression="gzip")

data_df.Metadata_genotype.value_counts()


# In[11]:


pd.crosstab(data_df.Metadata_genotype, data_df.Metadata_Well)


# ### PyBaSiC CellProfiler

# In[12]:


data_path = f"{output_dir}/nf1_sc_{method2}.csv.gz"
data_df = pd.read_csv(data_path, compression="gzip")

data_df.Metadata_genotype.value_counts()


# In[13]:


pd.crosstab(data_df.Metadata_genotype, data_df.Metadata_Well)


# ### PyBaSiC Cellpose

# In[14]:


data_path = f"{output_dir}/nf1_sc_{method3}.csv.gz"
data_df = pd.read_csv(data_path, compression="gzip")

data_df.Metadata_genotype.value_counts()


# In[15]:


pd.crosstab(data_df.Metadata_genotype, data_df.Metadata_Well)


# ### CellProfiler Cellpose

# In[16]:


data_path = f"{output_dir}/nf1_sc_{method4}.csv.gz"
data_df = pd.read_csv(data_path, compression="gzip")

data_df.Metadata_genotype.value_counts()


# In[17]:


pd.crosstab(data_df.Metadata_genotype, data_df.Metadata_Well)

