"""
This file contains functions to perform the splitting, cropping, and conversion of the second NF1 dataset using CellProfiler and
to reorder and rename the metadata of the images to fit the standard from the pilot dataset.
"""
import os
import pathlib
from pathlib import Path


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
        print("This plate has already been ran through CellProfiler!")


def rename_images(path_to_images: pathlib.Path, output_folder_name: str):
    """
    reorder and rename all images

    Parameters
    ----------
    path_to_images : pathlib.Path
        path to where the corrected images from CellProfiler are located
    output_folder_name:
        name of the folder with the outputed
    """
    original_prefix = ("DAPI", "GFP", "Actin")

    if any(
        images.name.startswith(original_prefix) for images in path_to_images.iterdir()
    ):
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
            print("The image names are reordered")
    else:
        print("This plate has already been reordered!")

    dapi_id = "DAPI"
    gfp_id = "GFP"
    actin_id = "Actin"

    keywords = (
        "01_1_1",
        "01_1_2",
        "01_1_3",
        "01_1_4",
        "01_2_1",
        "01_2_2",
        "01_2_3",
        "01_2_4",
        "01_3_1",
        "01_3_2",
        "01_3_3",
        "01_3_4",
    )

    for images in path_to_images.iterdir():
        if any(x in str(images) for x in keywords):
            print("The metadata for this plate has already been corrected!")
            break
        else:
            if dapi_id in str(images):
                DAPI_name = images.name.split("_")
                well = DAPI_name[0]
                site = DAPI_name[2]
                channel_name = DAPI_name[3]
                plate = DAPI_name[4].split(".")[0]

                new_DAPI_name = f"{output_folder_name}/{well}_01_1_{site}_{channel_name}_{plate}.tif"
                Path(images).rename(Path(new_DAPI_name))
                print(f"DAPI {well}_{site} image has been renamed")

            if gfp_id in str(images):
                GFP_name = images.name.split("_")
                well = GFP_name[0]
                site = GFP_name[2]
                channel_name = GFP_name[3]
                plate = GFP_name[4].split(".")[0]

                new_GFP_name = f"{output_folder_name}/{well}_01_2_{site}_{channel_name}_{plate}.tif"
                Path(images).rename(Path(new_GFP_name))
                print(f"GFP {well}_{site} image has been renamed")

            if actin_id in str(images):
                Actin_name = images.name.split("_")
                well = Actin_name[0]
                site = Actin_name[2]
                # replace Actin with RFP to keep metadata consistent between datasets
                channel_name = "RFP"
                plate = Actin_name[4].split(".")[0]

                new_Actin_name = f"{output_folder_name}/{well}_01_3_{site}_{channel_name}_{plate}.tif"
                Path(images).rename(Path(new_Actin_name))
                print(f"Actin (now RFP) {well}_{site} image has been renamed")
