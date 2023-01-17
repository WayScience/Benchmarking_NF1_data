#!/usr/bin/env python
# coding: utf-8

# # Create correlation heatmap from normalized and feature selected NF1 data

# ## Import libraries

# In[8]:


import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import seaborn as sb


# ## Read in NF1 data `csv`

# In[9]:


norm_fs_data = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_cellprofiler.csv.gz")

data = pd.read_csv(norm_fs_data, index_col=0)

print(data.shape)
data.head()


# ## Helper function to split `csv` into metadata and features

# In[10]:


def split_data(pycytominer_output: pd.DataFrame):
    """
    split pycytominer output to return metadata dataframe

    Parameters
    ----------
    pycytominer_output : pd.DataFrame
        dataframe with pycytominer output

    Returns
    -------
    pd.Dataframe, np.array
        metadata dataframe, feature_data
    """
    # split metadata from features
    metadata_cols = [
        col_name
        for col_name in pycytominer_output.columns.tolist()
        if "Metadata" in col_name
    ]
    metadata_dataframe = pycytominer_output[metadata_cols]
    feature_data = pycytominer_output[pycytominer_output.columns.difference(metadata_cols)]

    return metadata_dataframe, feature_data


# ## Split NF1 data `csv`

# In[11]:


metadata_dataframe, feature_data = split_data(data)
feature_data


# ## Transpose the NF1 dataframe

# In[12]:


data_trans = feature_data.transpose()
data_trans


# ## Create correlation heatmap

# In[13]:


data_trans_heatmap = sb.heatmap(data_trans.corr())

plt.show()

save_path = pathlib.Path("figures/correlation_heatmap_sc.png")
plt.savefig(save_path, bbox_inches="tight")


# ## Create clustermap with correlation heatmap

# In[14]:


sb.clustermap(data_trans.corr(), 
            cmap='RdBu_r',
            )

save_path = pathlib.Path("figures/correlation_clustermap_sc.png")
plt.savefig(save_path, bbox_inches="tight")

