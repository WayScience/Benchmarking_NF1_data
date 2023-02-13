from scipy.stats import ks_2samp
import pathlib
import pandas as pd

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
