#!/usr/bin/env python
# coding: utf-8

# # Perform Two-Sample KS-Test on NF1 Genotype Samples

# ## Import libraries

# In[1]:


import numpy as np
from scipy.stats import ks_2samp
import pathlib
import pandas as pd


# ## Set seed

# In[2]:


np.random.seed(0)


# ## Load in NF1 data

# In[3]:


norm_fs_data = pathlib.Path("../../../4_processing_features/data/nf1_sc_norm_cellprofiler.csv.gz")

data = pd.read_csv(norm_fs_data, compression="gzip", index_col=0)


# ## Helper functions to perform KS-test and create final `csv` file with results

# In[4]:


def nf1_ks_test_two_sample(data: pd.DataFrame):
    """seperate features by genotype and perform two sample ks-test on each feature

    Parameters
    ----------
    data : pd.Dataframe
        pycytominer output after normalization and feature selection

    Returns
    -------
    pd.Dataframe
        feature results from the two sample ks-test
    """
    feature_results = []

    null_features = data[(data["Metadata_genotype"] == "Null")]
    wt_features = data[(data["Metadata_genotype"] == "WT")]

    for column in data:
        if "Metadata" not in column:
            null_feature = null_features[column].to_numpy()
            wt_feature = wt_features[column].to_numpy()
            results = ks_2samp(wt_feature, null_feature)
            # have to seperate out namedtuple due to scipy hiding the last two results 
            results = tuple([results.statistic, results.pvalue, results.statistic_location, results.statistic_sign])
            feature_results.append(results)

    feature_results = pd.DataFrame(feature_results, columns=["statistic", "pvalue", "statistic_location", "statistic_sign"])

    return feature_results


def merge_features_kstest(
    feature_results: pd.DataFrame,
    column_names: list,
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
    dataframes = [column_names, feature_results]

    # merge dataframes together
    merged_dataframe = pd.concat(dataframes, axis=1)

    # save csv file if you would like
    if save_path is not None:
        merged_dataframe.to_csv(save_path, index=False)

    return merged_dataframe


# ## Peform two sample KS-test

# In[5]:


feature_results = nf1_ks_test_two_sample(data)
feature_results


# ## Take feature columns from data and create a list

# In[6]:


features = data.iloc[:,12:]
column_names = features.columns.tolist()
column_names = pd.DataFrame(column_names)
column_names.columns = ["Features"]

column_names


# ## Save the final `csv` file with merged features and results

# In[7]:


save_path = pathlib.Path("data/nf1_kstest_two_sample_results.csv")

merge_features_kstest(feature_results, column_names, save_path)

