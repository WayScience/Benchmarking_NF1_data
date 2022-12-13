"""
This file contains functions to perform the splitting, cropping, and conversion of the second NF1 dataset using CellProfiler and
to reorder and rename the metadata of the images to fit the standard from the pilot dataset.
"""
import os
import pathlib
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def correct_images(path_to_pipeline: str, path_to_output: str, path_to_images: str):
    """
    correct NF1 second plate with CellProfiler

    Parameters
    ----------
        path_to_pipeline (str): path to the CellProfiler .cppipe file
        path_to_output (str): path to the output folder for the corrected images
        path_to_images (str): path to folder with raw second plate images
    """
    if len(os.listdir(path_to_output)) == 0:
        # run CellProfiler on a plate that has not been analyzed yet (e.g. no files)
        command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} -i {path_to_images}"
        os.system(command)
    else:
        logging.warn("This plate has already been processed by CellProfiler!")


def rename_images(path_to_images: pathlib.Path, output_folder_name: str):
    """
    reorder and rename all images

    Parameters
    ----------
    path_to_images : pathlib.Path
        path to where the corrected images from CellProfiler are located
    output_folder_name:
        name of the folder with the outputted images
    """
    original_prefix = ("DAPI", "GFP", "Actin")

    # if any of the image names start with the channel name, then that means it needs to be reordered
    if any(
        images.name.startswith(original_prefix) for images in path_to_images.iterdir()
    ):
        # this splits the image names into individual metadata and reorders them to fit standard (as well as adding metadata)
        for images in path_to_images.iterdir():
            image_names = images.name.split("_")
            well = image_names[1]
            site = image_names[2]
            channel_name = image_names[0]
            plate = image_names[3].split(".")[0]
            new_image_name = (
                f"{output_folder_name}/{well}_01_{site}_{channel_name}_{plate}.tif"
            )
            Path(images).rename(Path(new_image_name))

        logging.info("The image names are reordered")

    # if the images do not have the prefix, then likely the image has already been processed so it should not be processed again
    # to avoid issues (e.g. wrongful reordering, deleting images, etc.)
    else:
        logging.warn("This plate has already been reordered!")

    channel_id_dict = {
        "DAPI": {"id": "01_1"},
        "GFP": {"id": "01_2"},
        "Actin": {"id": "01_3", "channel_name": "RFP"},
    }

    for image in path_to_images.iterdir():
        # checks if images have the correct length and if not do not proceed with renaming
        if len(image.name.split("_")) == 4:
            continue

        elif len(image.name.split("_")) != 4:
            logging.warn(f"The length is {len(image.name.split('_'))}. The expected lenth is 4. \nCheck to see if images are already renamed!")
            # logging.error(f"The length is {len(image.name.split('_'))}")
            # ADD EXCEPTION
            break

        # goes through keys within dictionary
        for channel in channel_id_dict.keys():
            channel_id = channel_id_dict[channel]["id"]
            if "channel_name" in channel_id_dict[channel].keys():
                channel_name = channel_id_dict[channel]["channel_name"]
            else:
                channel_name = channel

            if channel in str(image):
                well, _, site, _, plate = image.name.split("_")
                plate = plate.split(".")[0]

                new_channel_name = f"{output_folder_name}/{well}_{channel_id}_{site}_{channel_name}_{plate}.tif"
                Path(image).rename(Path(new_channel_name))

        logging.info("All channels in this plate have been renamed!")
    
