import pathlib
import pandas as pd

def add_sc_count_metadata(data_path:pathlib.Path): 
    """
    This function loads in the saved csv from Pycytominer (e.g. normalized, etc.), adds the single cell counts for
    each well as metadata, and saves the csv to the same place (as a csv.gz file)
    
    Parameters
    ----------
    data_path : pathlib.Path
        path to the csv.gz files outputted from Pycytominer (this is the same path as the output path)
    """
    data_df = pd.read_csv(data_path, compression="gzip")

    merged_data = data_df.groupby(["Metadata_Well"])['Metadata_Well'].count().reset_index(name='Metadata_number_of_singlecells')

    data_df = data_df.merge(merged_data, on="Metadata_Well")
    # pop out the column from the dataframe
    singlecell_column = data_df.pop('Metadata_number_of_singlecells')
    # insert the column as the second index column in the dataframe
    data_df.insert(2, 'Metadata_number_of_singlecells', singlecell_column)

    data_df.to_csv(data_path)
