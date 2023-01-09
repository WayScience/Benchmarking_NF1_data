#!/usr/bin/env python
# coding: utf-8

# # Create 2D UMAP using genotype

# ## Import libraries

# In[1]:


import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.colors import rgb2hex
from mpl_toolkits.mplot3d import axes3d, Axes3D
import umap

import UMAPutils as utils


# ## Create random seed

# In[2]:


# make random np operations reproducible
np.random.seed(0)


# ## Set paths

# In[3]:


embeddings_path = pathlib.Path("../../data/norm_fs_embeddings.csv.gz")
embeddings_data = pd.read_csv(embeddings_path, compression="gzip", index_col=0)


# ## Create 2D UMAP

# In[4]:


plt.figure(figsize=(15, 12))

# Produce scatterplot with umap data, using metadata to color points
sns_plot = sns.scatterplot(
    data=embeddings_data,
    x=embeddings_data['UMAP1'],
    y=embeddings_data['UMAP2'],
    hue=embeddings_data["Metadata_genotype"]
)
# Adjust legend
sns_plot.legend(
    loc="center left", bbox_to_anchor=(1, 0.5), title='genotype'
)
# Label axes, title
sns_plot.set_xlabel("UMAP 1")
sns_plot.set_ylabel("UMAP 2")
sns_plot.set_title("2 Dimensional UMAP")

save_path = pathlib.Path("UMAPs/2D_umap_nf1_genotype.png")

plt.savefig(save_path, bbox_inches="tight")

