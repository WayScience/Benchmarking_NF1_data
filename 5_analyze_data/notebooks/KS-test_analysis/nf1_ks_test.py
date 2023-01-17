#!/usr/bin/env python
# coding: utf-8

# # Perform Two-Sample KS-Test on NF1 Genotype Samples

# ## Import libraries

# In[15]:


import numpy as np
from scipy.stats import ks_2samp
import pathlib
import pandas as pd


# ## Set seed

# In[16]:


np.random.seed(0)


# ## Load in NF1 data

# In[17]:


norm_fs_data = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_cellprofiler.csv.gz")

data = pd.read_csv(norm_fs_data, compression="gzip", index_col=0)

print(data.shape)
data.head()


# ## Helper functions to perform KS-test and create final `csv` file with results

# In[18]:


def nf1_ks_test_two_sample(normalized_data: pd.DataFrame):
    """separate features by genotype and perform two sample ks-test on each feature

    Parameters
    ----------
    normalized_data : pd.Dataframe
        pycytominer output after normalization

    Returns
    -------
    pd.Dataframe
        feature results from the two sample ks-test
    """
    feature_results = []

    # divide the NF1 data based on genotype
    null_features = normalized_data[(normalized_data["Metadata_genotype"] == "Null")]
    wt_features = normalized_data[(normalized_data["Metadata_genotype"] == "WT")]

    # iterate through the columns in the data (both of the genotype dataframes will have the same columns)
    for column in normalized_data:
        # do not include metadata columns
        if "Metadata" not in column:
            # convert each individual column (feature) into numpy array
            null_feature = null_features[column].to_numpy()
            wt_feature = wt_features[column].to_numpy()
            
            # run two-sample ks-test for each feature 
            results = ks_2samp(wt_feature, null_feature)
            # convert all keys/ks-test results (even the hidden ones due to scipy) into a dictionary 
            # and put them as a list
            results = tuple(list(results._asdict().values()))
            feature_results.append(results)

    feature_results = pd.DataFrame(feature_results, columns=["statistic", "pvalue", "statistic_location", "statistic_sign"])

    return feature_results

def merge_features_kstest(
    feature_results: pd.DataFrame,
    feature_names: list,
    save_path: pathlib.Path = None,
):
    """
    merge features with ks-test results into one dataframe

    Parameters
    ----------
    feature_results : pd.Dataframe
        ks-test results
    column_names : list
        feature names from the columns of the NF1 data
    save_path : pathlib.Path
        path for the new dataframe

    Returns
    -------
    pd.Dataframe
        merged dataframe with features and ks-test results
    """
    # put dataframes into list of where the columns should go
    dataframes = [feature_names, feature_results]

    # merge dataframes together
    merged_dataframe = pd.concat(dataframes, axis=1)

    # save csv file if you would like
    if save_path is not None:
        merged_dataframe.to_csv(save_path, index=False)

    return merged_dataframe


# ## Perform two sample KS-test

# In[19]:


feature_results = nf1_ks_test_two_sample(data)
feature_results


# ## Take feature columns from data and create a list

# In[20]:


# find feature names in the columns from the data
feature_names = [
        col_name
        for col_name in data.columns.tolist()
        if "Metadata" not in col_name
    ]

feature_names = pd.DataFrame(feature_names)
feature_names.columns = ["Features"]

feature_names


# ## Save the final `csv` file with merged features and results

# In[21]:


save_path = pathlib.Path("data/nf1_kstest_two_sample_results.csv")

merge_features_kstest(feature_results, feature_names, save_path)

