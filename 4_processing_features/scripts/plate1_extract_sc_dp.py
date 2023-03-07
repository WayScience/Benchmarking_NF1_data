#!/usr/bin/env python
# coding: utf-8

# # Process single cell morphology features for DeepProfiler readouts - Plate 1

# ## Import libraries

# In[1]:


import pathlib

from pycytominer import feature_select
from pycytominer.cyto_utils import DeepProfiler_processing, output, infer_cp_features


# ## Set paths to DP project

# In[2]:


dp_output_nuc = pathlib.Path("../3_extracting_features/NF1_nuc_project-DP")
dp_output_cyto = pathlib.Path("../3_extracting_features/NF1_cyto_project-DP")

index_file_nuc = pathlib.Path(f"{dp_output_nuc}/inputs/metadata/index.csv")
index_file_cyto = pathlib.Path(f"{dp_output_cyto}/inputs/metadata/index.csv")

profile_dir_nuc = pathlib.Path(f"{dp_output_nuc}/outputs/efn_pretrained/features")
profile_dir_cyto = pathlib.Path(f"{dp_output_cyto}/outputs/efn_pretrained/features")


# ## Set paths to outputs

# In[3]:


output_dir = pathlib.Path('data')

output_file_raw_nuc = pathlib.Path(f'{output_dir}/nf1_sc_deepprofiler_nuc.csv.gz')
output_file_raw_cyto = pathlib.Path(f'{output_dir}/nf1_sc_deepprofiler_cyto.csv.gz')

output_file_norm_nuc = pathlib.Path(f'{output_dir}/nf1_sc_norm_deepprofiler_nuc.csv.gz')
output_file_norm_cyto = pathlib.Path(f'{output_dir}/nf1_sc_norm_deepprofiler_cyto.csv.gz')

output_file_norm_fs_nuc = pathlib.Path(f'{output_dir}/nf1_sc_norm_fs_deepprofiler_nuc.csv.gz')
output_file_norm_fs_cyto = pathlib.Path(f'{output_dir}/nf1_sc_norm_fs_deepprofiler_cyto.csv.gz')


# ## Perform normalization and feature selection on DP Nuclei project

# ### Create DeepProfilerData object

# In[4]:


deep_data_nuc = DeepProfiler_processing.DeepProfilerData(
    index_file_nuc, profile_dir_nuc, filename_delimiter="/", file_extension=".npz"
)


# ### Initalize SingleCellDeepProfiler class

# In[5]:


deep_single_cell_nuc = DeepProfiler_processing.SingleCellDeepProfiler(deep_data_nuc)


# ### Compile raw single cell data

# In[6]:


nuc_sc = deep_single_cell_nuc.get_single_cells(output=True, location_x_col_index=1, location_y_col_index=2)
output(nuc_sc, output_file_raw_nuc)

print(nuc_sc.shape)
nuc_sc.head()


# ### Normalize raw single cell data

# In[7]:


normalized_nuc = deep_single_cell_nuc.normalize_deep_single_cells(
    output_file=output_file_norm_nuc, location_x_col_index=1, location_y_col_index=2
)

print(normalized_nuc.shape)
normalized_nuc.head()


# ### Separate metadata and features prior to feature selection

# In[8]:


# extract metadata prior to feature selection
metadata_cols = infer_cp_features(normalized_nuc, metadata=True)
derived_features = [
    x for x in normalized_nuc.columns.tolist() if x not in metadata_cols
]


# ### Feature selection from normalized data

# In[9]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
]

feature_select_norm_nuc = feature_select(
    normalized_nuc,
    features = derived_features,
    operation= feature_select_ops,
)

output(feature_select_norm_nuc, output_file_norm_fs_nuc)

print(feature_select_norm_nuc.shape)
feature_select_norm_nuc.head()


# ## Perform normalization and feature selection on DP Nuclei project

# ### Create DeepProfilerData object

# In[10]:


deep_data_cyto = DeepProfiler_processing.DeepProfilerData(
    index_file_cyto, profile_dir_cyto, filename_delimiter="/", file_extension=".npz"
)


# ### Initialize SingleDeepProfiler class

# In[11]:


deep_single_cell_cyto = DeepProfiler_processing.SingleCellDeepProfiler(deep_data_cyto)


# ### Compile raw single cell data

# In[12]:


cyto_sc = deep_single_cell_cyto.get_single_cells(output=True, location_x_col_index=1, location_y_col_index=2)
output(cyto_sc, output_file_raw_cyto)

print(cyto_sc.shape)
cyto_sc.head()


# ### Normalize raw single cell data

# In[13]:


normalized_cyto = deep_single_cell_cyto.normalize_deep_single_cells(
    output_file=output_file_norm_cyto, location_x_col_index=1, location_y_col_index=2
)

print(normalized_cyto.shape)
normalized_cyto.head()


# ### Separate metadata and features prior to feature selection

# In[14]:


# extract metadata prior to feature selection
metadata_cols = infer_cp_features(normalized_cyto, metadata=True)
derived_features = [
    x for x in normalized_cyto.columns.tolist() if x not in metadata_cols
]


# ### Feature selection from normalized data

# In[15]:


feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
]

feature_select_norm_cyto = feature_select(
    normalized_cyto,
    features = derived_features,
    operation= feature_select_ops,
)

output(feature_select_norm_cyto, output_file_norm_fs_cyto)

print(feature_select_norm_cyto.shape)
feature_select_norm_cyto.head()

