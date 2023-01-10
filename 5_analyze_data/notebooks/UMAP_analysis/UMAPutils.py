"""
This file contains functions to assist in creating a .csv file containing 2D embeddings from 
the NF1 normalized and feature selected morphological readouts.
"""

import pathlib
import pandas as pd

def split_data(pycytominer_output: pd.DataFrame):
    """
    split pycytominer output to metadata dataframe and np array of feature values

    Parameters
    ----------
    pycytominer_output : pd.DataFrame
        dataframe with pycytominer output

    Returns
    -------
    pd.Dataframe, np.ndarray
        metadata dataframe, feature values
    """
    # split metadata from features
    metadata_cols = [
        col_name
        for col_name in pycytominer_output.columns.tolist()
        if "Metadata" in col_name
    ]
    metadata_dataframe = pycytominer_output[metadata_cols]

    feature_cols = [
        col_name
        for col_name in pycytominer_output.columns.tolist()
        if "Metadata" not in col_name
    ]
    feature_data = pycytominer_output[feature_cols].values

    return metadata_dataframe, feature_data


def merge_metadata_embeddings(
    metadata_dataframe: pd.DataFrame, embeddings: pd.DataFrame, save_path: pathlib.Path = None
):
    """
    merge metadata with UMAP embeddings into one dataframe

    Parameters
    ----------
    metadata_dataframe : pd.Dataframe
        metadata for the NF1 single cells
    embeddings : pd.Dataframe
        2D UMAP embeddings for the x,y coordinates for each single cell

    Returns
    -------
    pd.Dataframe
        merged dataframe with metadata and embeddings
    """
    # reset index to remove the 'Metadata_WellRow' as the index then drop the index
    metadata_dataframe = metadata_dataframe.reset_index()
    metadata_dataframe = metadata_dataframe.reset_index(drop=True)

    # remove index from embeddings dataframe as well to prevent IndexError
    embeddings = embeddings.reset_index(drop=True)

    # put dataframes into list of where the columns should go
    dataframes = [metadata_dataframe, embeddings]

    # merge dataframes together
    merged_dataframe = pd.concat(dataframes, axis=1)

    # save csv file if you would like
    if save_path is not None:
        merged_dataframe.to_csv(save_path, index=False)

    return merged_dataframe
