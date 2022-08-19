# from cellpose.io import logger_setup
from cellpose import models, core, io, utils
from typing import Tuple

import pathlib
import pandas as pd
import skimage.io as io

import cv2
import numpy as np

import matplotlib.path as mplPath


def get_seg_data(image: np.ndarray, model_specs: dict, seg_data_output: str) -> pd.DataFrame:
    """finds center X,Y or outlines of objects using cellpose specs from model_specs and return pandas array with the specified data of objects
    Args:
        image (np.ndarray): image with objects to segment
        model_specs (dict): specifications for cellpose segmentation
        data (str): specified segmentation data information for an object, either "locations" or "outlines"
    Returns:
        pd.DataFrame: dataframe with object data
    """
    # Empty list for object data
    objects_data = []

    # CellPose model has many different parameters that can be found via the Command Line documentation (https://cellpose.readthedocs.io/en/latest/command.html), which
    # can then be found for Python implementation using the CellPose GitHub (https://github.com/MouseLand/cellpose/tree/main/cellpose.)
    cellpose_model = models.Cellpose(gpu=True, model_type=model_specs["model_type"])
    masks, flows, styles, diams = cellpose_model.eval(
        image,
        diameter=model_specs["diameter"],
        channels=model_specs["channels"],
        flow_threshold=model_specs["flow_threshold"],
    )

    # Remove the cell masks that are on the edges of the image
    if model_specs["remove_edge_masks"]:
        masks = utils.remove_edge_masks(masks)

    # If `data` is set to locations, then the (x,y) points that create the outlines for each of the cells being segmented that is determined by CellPose will be used 
    # to calculate the mean of the outline points. The mean is the (x,y) center coordinates and is added into the objects data list from above.
    if seg_data_output == 'locations':
        outlines = utils.outlines_list(masks)
        for outline in outlines:
            centroid = outline.mean(axis=0)
            object_data = {
                "Location_Center_X": centroid[0],
                "Location_Center_Y": centroid[1],
            }
            objects_data.append(object_data)

    # If `data` is set to outlines, the (x,y) points that make the outlines for the object will be appended to the list for each well and site.
    if seg_data_output == 'outlines':
        outlines = utils.outlines_list(masks)
        for outline in outlines:
            object_data = {
                "Outline": outline,
            }
            objects_data.append(object_data)


    # Covert the object data list into a pandas Dataframe
    objects_data = pd.DataFrame(objects_data)
    return objects_data

def overlay_channels(identifier: str, images_dir: pathlib.Path, rfp_multiplier: int = 1, gfp_multiplier: int = 1, dapi_multiplier: int = 1):
    """overlays cytoplasm, ER, and nuclei channels to help cytoplasm segmentation in CellPose

    Args:
        current_image (str): string for current site to overlay the channels for
        current_dir (pathlib.Path): directory of where the current images used are located
        rfp_multiplier (int): integer to multiply to the rfp channel if you want these objects brighter for human visual interpretation (default = 1, no change)
        gfp_multiplier (int): integer to multiply to the gfp channel if you want these objects brighter for human visual interpretation (default = 1, no change)
        dapi_multiplier (int): integer to multiply to the dapi channel if you want these objects brighter for human visual interpretation (default = 1, no change)
    """
    # Takes the identifer of the nuclei channel and splits it into parts: well, plate, channel, site
    # We then use all parts except for channel and change it for the GFP and RFP IDs
    field_details = identifier.split("_")

    dapi_id = identifier
    gfp_id = f"{field_details[0]}_{field_details[1]}_2_{field_details[3]}"
    rfp_id = f"{field_details[0]}_{field_details[1]}_3_{field_details[3]}"

    # Iterate through the directory containing the images and if an image has the ID of the given channel, it will read in that image. There are three images total
    # that are read in for each site that needs to be overlayed
    for image_path in images_dir.iterdir():
        if dapi_id in image_path.name:
            dapi = io.imread(image_path)
        if gfp_id in image_path.name:
            gfp = io.imread(image_path)
        if rfp_id in image_path.name:
            rfp = io.imread(image_path)

    # RFP = red channel (cytoplasm), GFP = green channel (ER), DAPI = blue (nuclei)
    # Multiplier only assists in user interpretation of the images to configure model parameters in CellPose GUI
    # CellPose does not take the multipliers into consideration when performing segmentation
    overlay = np.dstack([rfp * rfp_multiplier, gfp * gfp_multiplier, dapi * dapi_multiplier])

    return overlay


def get_nuc_cyto_data(
    nuc_locations: pd.DataFrame, cyto_outlines: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """creates nuclei and cytoplasm dataframes with corresponding cell IDs from nuclei locations and cytoplasm outlines
    Args:
        nuc_locations (pd.DataFrame): dataframe with nuclei center coords for certain image
        cyto_outlines (pd.DataFrame): dataframe with cytoplasm outline for same image as above
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: nuc_data and cyto_data with corresponding cell IDs and center coords for each object
    """
    # Empty lists for the nuclei and cytoplasm data
    nuc_data = []
    cyto_data = []

    # add Cell_ID column from index to the cyto_outlines dataframe where each each index value is the Cell_ID number
    cyto_outlines = cyto_outlines.reset_index()
    cyto_outlines = cyto_outlines.rename(columns={"index": "Cell_ID"})

    # Iterate over all cytoplasm outlines
    for cyto_index, cyto_row in cyto_outlines.iterrows():
        cell_id = cyto_row["Cell_ID"]

        # Create path (polygon) from outlines that is used to check if the nuclei are in this path
        outline = cyto_row["Outline"]
        cytoplasm_path = mplPath.Path(outline)

        # Check if any of the nuclei are within cytoplasm path
        for nuc_index, nuc_row in nuc_locations.iterrows():
            nuc_center = (nuc_row["Location_Center_X"], nuc_row["Location_Center_Y"])
            # If nuclei (one or more) is in cytoplasm path, this gives it same cell ID as cytoplasm that it is within
            if cytoplasm_path.contains_point(nuc_center):
                current_nuc_data = {
                    "Cell_ID": cell_id,
                    "Location_Center_X": nuc_row["Location_Center_X"],
                    "Location_Center_Y": nuc_row["Location_Center_Y"],
                }
                nuc_data.append(current_nuc_data)

                # Drop nucleus once it has been identfied in a cytoplasm so isn't rechecked
                nuc_locations.drop(nuc_index, inplace=True)

                # Convert cytoplasm outlines to center coords
                centroid = cyto_row["Outline"].mean(axis=0)
                current_cyto_data = {
                    "Cell_ID": cell_id,
                    "Location_Center_X": centroid[0],
                    "Location_Center_Y": centroid[1],
                    "Outline": cyto_row["Outline"].tolist(),
                }
                cyto_data.append(current_cyto_data)

    # Creates a pandas dataframe for nuc_data and cyto_data using the dicts created within the function
    nuc_data = pd.DataFrame.from_dict(nuc_data)
    cyto_data = pd.DataFrame.from_dict(cyto_data)

    # Drop duplicates from cyto_data because cytoplasm is added into multiple rows if it contains more than one nuclei
    cyto_data = cyto_data.drop_duplicates(subset="Cell_ID")

    return nuc_data, cyto_data


def segment_NF1(
    data_path: pathlib.Path,
    save_path: pathlib.Path,
    nuclei_model_specs: dict,
    cyto_model_specs: dict,
):
    """segments NF1 data from data_path and save segmentation data in save_path using specified cellpose_model

    Args:
        data_path (pathlib.Path): load path for cell health data
        save_path (pathlib.Path): save path for segmentation data
        cellpose_model_nuclei (models.Cellpose): cellpose model to use for segmenting nuclei
        cellpose_model_actin (models.Cellpose): cellpose model to use for segmentating actin
    """
    # Iterate through folder with images and create paths to images with DAPI in name
    for image_path in data_path.iterdir():
        if "DAPI" in image_path.name:
            nuc_save_path = f"{save_path}/{image_path.name}"
            # Convert string into pathlib.Path -> strings do not have names so need to convert
            nuc_save_path = pathlib.Path(nuc_save_path)

            # Take the nuc_save_path name and split it into the individual parts (well, plate, channel, site) and removes the rest
            image_details = nuc_save_path.name.split("_")[0:4]
            # Then join the parts that are necessary for identification to use later
            image_identifier = "_".join(image_details)

            # Split the identifier into parts and find the well and site
            field_details = image_identifier.split("_")
            well = f"{field_details[0]}"
            site = f"{field_details[3]}"
            identifier = f"{well}_{site}"

            # Create pathlib.Path that uses the save_path along with the well and site to create the name for the new .tsv file for nuclei
            nuc_save_path = pathlib.Path(f"{save_path}/{well}_{site}_nuc-segmented.tsv")

            # If the nuc-segmented.tsv file is not already a file, then proceed through the full segmentation pipeline
            if not nuc_save_path.is_file():

                print(f"Segmenting {nuc_save_path.name}")

                # Load in images that with DAPI
                nuc_save_path.parents[0].mkdir(parents=True, exist_ok=True)
                nuc_image = io.imread(image_path)
                nuc_locations = get_seg_data(nuc_image, nuclei_model_specs, seg_data_output='locations')
                # nuc_locations.to_csv(nuc_save_path, sep="\t")

                # Create save path for cytoplasm with a specific suffix
                cyto_save_path = f"{save_path}/{well}_{site}_cyto-segmented.tsv"
                cyto_save_path = pathlib.Path(cyto_save_path)

                # Segment cytoplasm outlines by overlaying the channels for each site and finding outlines from those images
                print(f"Segmenting {cyto_save_path.name}")
                overlay_image = overlay_channels(image_identifier, data_path)
                cyto_outlines = get_seg_data(overlay_image, cyto_model_specs, seg_data_output='outlines')
                # cyto_outlines.to_csv(cyto_save_path, sep="\t")

                # Take the nuclei locations and cytoplasm outlines to link Cell_IDs for each to nuclei to their respective cytoplasm
                nuc_data, cyto_data = get_nuc_cyto_data(nuc_locations, cyto_outlines)

                # Save each of the center coords for the cells from each site
                nuc_data.to_csv(nuc_save_path, sep="\t", index=False)
                cyto_data.to_csv(cyto_save_path, sep="\t", index=False)

            else:
                print(f"{identifier} already exists!")
