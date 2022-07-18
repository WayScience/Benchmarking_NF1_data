#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import matplotlib.pyplot as plt

import skimage.io
import skimage.exposure
import skimage.measure

import xarray as xr

import starfish
import starfish.data
from starfish.types import Axes
from starfish.image import Filter

from PIL import Image

get_ipython().run_line_magic('matplotlib', 'inline')


# In[19]:


experiment = starfish.data.ISS(use_test_data=True)
image: starfish.ImageStack = experiment['fov_001'].get_image('primary')


# In[24]:


experiment


# In[20]:


masking_radius = 5
filt = Filter.WhiteTophat(masking_radius, is_volume=False)
filtered = filt.run(image, verbose=True, in_place=False)

orig_plot: xr.DataArray = image.sel({Axes.CH: 0, Axes.ROUND: 0}).xarray.squeeze()
wth_plot: xr.DataArray = filtered.sel({Axes.CH: 0, Axes.ROUND: 0}).xarray.squeeze()

f, (ax1, ax2) = plt.subplots(ncols=2)
ax1.imshow(orig_plot)
ax1.set_title("original")
ax2.imshow(wth_plot)
ax2.set_title("wth filtered")


# In[18]:



masking_radius = 5
filt = Filter.WhiteTophat(masking_radius, is_volume=False)
filtered = filt.run(image, verbose=True, in_place=False)

orig_plot: xr.DataArray = image.sel({Axes.CH: 0, Axes.ROUND: 0}).xarray.squeeze()
wth_plot: xr.DataArray = filtered.sel({Axes.CH: 0, Axes.ROUND: 0}).xarray.squeeze()

f, (ax1, ax2) = plt.subplots(ncols=2)
ax1.imshow(orig_plot)
ax1.set_title("original")
ax2.imshow(wth_plot)
ax2.set_title("wth filtered")


# In[ ]:




