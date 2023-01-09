#!/usr/bin/env python
# coding: utf-8

# # Get 2D UMAP embeddings for NF1 data

# ## Import libraries

# In[1]:


import pathlib
import pandas as pd
import seaborn as sns
from matplotlib.colors import rgb2hex
from mpl_toolkits.mplot3d import axes3d, Axes3D
import umap

import sys
sys.path.append("../")
import UMAPutils as utils


# ## Set paths

# In[2]:


norm_data_path = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_fs_cellprofiler.csv.gz")
norm_data = pd.read_csv(norm_data_path, compression="gzip", index_col=0)

metadata_dataframe, feature_data = utils.split_data(norm_data)


# ## Get embeddings as a pandas dataframe

# In[3]:


fit = umap.UMAP(random_state=0, n_components=2)

embeddings = pd.DataFrame(
        fit.fit_transform(feature_data), columns=["UMAP1", "UMAP2"]
    )
embeddings


# ## Combine metadata with embeddings and save as new `.csv.gz` file

# In[4]:


save_path = pathlib.Path('../../data/norm_fs_embeddings.csv.gz')

norm_fs_embeddings_data = utils.merge_metadata_embeddings(metadata_dataframe, embeddings, save_path)
norm_fs_embeddings_data

