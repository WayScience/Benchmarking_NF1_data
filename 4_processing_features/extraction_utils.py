import pathlib
import pandas as pd

from pycytominer import normalize, feature_select
from pycytominer.cyto_utils import cells, output


def extract_single_cells(
    single_cell_file: str,
    linking_cols: dict,
    platemap_df: pd.DataFrame,
    output_folder: str,
    method_name: str,
    normalize_sc: bool = False,
    feature_selection_sc: bool = False,
    norm_feature_select: bool = False,
):
    """use Pycytominer SingleCells class to perform single cell extraction, normalization, and feature selection on
    CellProfiler SQLite files. Normalization and feature selection are optional processes that you can choose
    to turn on. This function will output all data into individual csv.gz files to a specified output folder.

    Args:
        single_cell_file (str):
            file path to SQLite file (must start with sqlite:///)
        linking_cols (dict):
            dictionary with the linking columns between compartments/tables in database
        platemap_df (pd.DataFrame):
            dataframe with the platemap metadata to merge with single cells
        output_folder (str):
            path to output folder for csv.gz files
        method_name (str):
            name of pipeline method used for naming the output files
        normalize_sc (bool, optional):
            if set to True, this will perform normalization on the raw merged single cell data (defaults to False)
        feature_selection_sc (bool, optional):
            if set to True, this will perform feature extraction on raw merged single cell data (defaults to False)
        norm_feature_select (bool, optional):
            if set to True, this will perform normalization on raw merged single cell data and feature extraction on
            the normalizated data (defaults to False)
    """
    # instaniate the SingleCells class
    sc = cells.SingleCells(
        sql_file=single_cell_file,
        compartments=["Per_Cells", "Per_Cytoplasm", "Per_Nuclei"],
        compartment_linking_cols=linking_cols,
        image_table_name="Per_Image",
        strata=["Image_Metadata_Well", "Image_Metadata_Plate"],
        merge_cols=["ImageNumber"],
        image_cols="ImageNumber",
        load_image_data=True,
    )

    # Merge single cells across compartments based on well
    anno_kwargs = {"join_on": ["Metadata_well_position", "Image_Metadata_Well"]}

    sc_df = sc.merge_single_cells(
        platemap=platemap_df,
        **anno_kwargs,
    )

    sc_output_file = pathlib.Path(f"{output_folder}/nf1_sc_{method_name}.csv.gz")

    # Save level 2 data as a csv
    output(sc_df, sc_output_file)

    # Perform normalization on the raw extracted single cell data
    if normalize_sc == True:
        # Normalize single cell data and write to file
        normalize_sc_df = normalize(sc_df, method="standardize")

        sc_norm_output_file = pathlib.Path(
            f"{output_folder}/nf1_sc_norm_{method_name}.csv.gz"
        )

        output(normalize_sc_df, sc_norm_output_file)

    # Perform feature selection on the raw extracted single cell data
    if feature_selection_sc == True:
        # Select features that will show significant difference between genotypes
        feature_select_ops = [
            "variance_threshold",
            "correlation_threshold",
            "blocklist",
        ]

        feature_select_norm_sc_df = feature_select(sc_df, operation=feature_select_ops)

        sc_norm_fs_output_file = pathlib.Path(
            f"{output_folder}/nf1_sc_norm_fs_{method_name}.csv.gz"
        )

        output(feature_select_norm_sc_df, sc_norm_fs_output_file)

    # Perform normalization on raw extracted single cells and perform feature selection on the normalized data
    if norm_feature_select == True:
        # Normalize single cell data and write to file
        normalize_sc_df = normalize(sc_df, method="standardize")

        sc_norm_output_file = pathlib.Path(
            f"{output_folder}/nf1_sc_norm_{method_name}.csv.gz"
        )

        output(normalize_sc_df, sc_norm_output_file)

        # Select features that will show significant difference between genotypes
        feature_select_ops = [
            "variance_threshold",
            "correlation_threshold",
            "blocklist",
        ]

        feature_select_norm_sc_df = feature_select(
            normalize_sc_df, operation=feature_select_ops
        )

        sc_norm_fs_output_file = pathlib.Path(
            f"{output_folder}/nf1_sc_norm_fs_{method_name}.csv.gz"
        )

        output(feature_select_norm_sc_df, sc_norm_fs_output_file)
