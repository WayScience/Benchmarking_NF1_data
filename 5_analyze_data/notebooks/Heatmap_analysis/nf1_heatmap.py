#!/usr/bin/env python
# coding: utf-8

# # Create correlation heatmap from normalized and feature selected NF1 data

# ## Import libraries

# In[1]:


import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import seaborn as sb

import sys
sys.path.append("../UMAP_analysis/")
import UMAPutils as utils


# ## Read in NF1 data `csv`

# In[2]:


norm_fs_data = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_cellprofiler.csv.gz")

data = pd.read_csv(norm_fs_data, index_col=0)

print(data.shape)
data.head()


# ## Split NF1 data `csv`

# In[3]:


metadata_dataframe, feature_data = utils.split_data(data)
feature_data


# ## Transpose the NF1 dataframe

# In[4]:


data_trans = feature_data.transpose()
data_trans


# ## Create correlation heatmap

# In[5]:


data_trans_heatmap = sb.heatmap(data_trans.corr())

plt.show()

save_path = pathlib.Path("figures/correlation_heatmap_sc.png")
plt.savefig(save_path, bbox_inches="tight")


# ## Create clustermap with correlation heatmap

# In[6]:


sb.clustermap(data_trans.corr(), 
            cmap='RdBu_r',
            )

save_path = pathlib.Path("figures/correlation_clustermap_sc.png")
plt.savefig(save_path, bbox_inches="tight")

