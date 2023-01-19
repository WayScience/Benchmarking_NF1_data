#!/usr/bin/env python
# coding: utf-8

# # Create correlation heatmap from normalized and feature selected NF1 data for both CellProfiler and DeepProfiler

# ## Import libraries

# In[1]:


import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import seaborn as sb

import sys
sys.path.append("../UMAP_analysis/")
import UMAPutils as utils


# ## CellProfiler data

# ### Read in NF1 data `csv`

# In[2]:


norm_fs_data = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_cellprofiler.csv.gz")

data = pd.read_csv(norm_fs_data, index_col=0)

print(data.shape)
data.head()


# ### Split NF1 data `csv`

# In[3]:


metadata_dataframe, feature_data = utils.split_data(data)
feature_data


# ### Transpose the NF1 dataframe

# In[4]:


data_trans = feature_data.transpose()
data_trans


# ### Create correlation heatmap

# In[5]:


data_trans_heatmap = sb.heatmap(data_trans.corr())

plt.show()

save_path = pathlib.Path("figures/correlation_heatmap_sc.png")
plt.savefig(save_path, bbox_inches="tight")


# ### Create clustermap with correlation heatmap

# In[6]:


sb.clustermap(data_trans.corr(), 
            cmap='RdBu_r',
            )

save_path = pathlib.Path("figures/correlation_clustermap_sc.png")
plt.savefig(save_path, bbox_inches="tight")


# ## DeepProfiler data

# In[7]:


norm_fs_data_nuc = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_deepprofiler_nuc.csv.gz")
norm_fs_data_cyto = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_deepprofiler_cyto.csv.gz")

data_nuc = pd.read_csv(norm_fs_data_nuc)
data_cyto = pd.read_csv(norm_fs_data_cyto)

print(data_nuc.shape)
data_nuc.head()


# In[8]:


metadata_dataframe_nuc, feature_data_nuc = utils.split_data(data_nuc)

feature_data_nuc = feature_data_nuc.drop(['Location_Center_X', 'Location_Center_Y'], axis=1)

print(feature_data_nuc.shape)
feature_data_nuc.head()


# In[9]:


metadata_dataframe_cyto, feature_data_cyto = utils.split_data(data_cyto)

feature_data_cyto = feature_data_cyto.drop(['Location_Center_X', 'Location_Center_Y'], axis=1)

print(feature_data_cyto.shape)
feature_data_cyto.head()


# In[10]:


data_trans_nuc = feature_data_nuc.transpose()
data_trans_cyto = feature_data_cyto.transpose()

print(data_trans_nuc.shape)
data_trans_nuc.head()


# In[11]:


data_trans_nuc_heatmap = sb.heatmap(data_trans_nuc.corr())

plt.show()


# In[12]:


data_trans_cyto_heatmap = sb.heatmap(data_trans_cyto.corr())

plt.show()


# In[13]:


sb.clustermap(data_trans_nuc.corr(), 
            cmap='RdBu_r',
            )

save_path = pathlib.Path("figures/correlation_clustermap_sc_dp_nuc.png")
plt.savefig(save_path, bbox_inches="tight")


# In[14]:


sb.clustermap(data_trans_cyto.corr(), 
            cmap='RdBu_r',
            )

save_path = pathlib.Path("figures/correlation_clustermap_sc_dp_cyto.png")
plt.savefig(save_path, bbox_inches="tight")


# In[ ]:




