from importlib.resources import path
import pandas as pd
import pathlib
from pathlib import Path
import shutil

from PIL import Image
import os


def copy_DP_files(
    project_path: pathlib.Path, config_name: str, checkpoint_name: str,
):
    """Copy config and checkpoint files to their designated location in DP project as assigned by the project_path. This is important
    to have the files copied in the specific format within this function for DeepProfiler to run.
    Args:
        project_path (pathlib.Path): Path for DP project to be located in
        config_name (str): Name of config file to copy
        checkpoint_name (str): Name of checkpoint file to copy
    """

    # Copy config file to DP project
    config_load_path = pathlib.Path(f"DP_files/{config_name}")
    config_save_path = pathlib.Path(f"{project_path}/inputs/config/{config_name}")
    config_save_path.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(config_load_path, config_save_path)

    # Copy checkpoint file to DP project
    checkpoint_load_path = pathlib.Path(f"DP_files/{checkpoint_name}")
    checkpoint_save_path = pathlib.Path(
        f"{project_path}/outputs/efn_pretrained/checkpoint/{checkpoint_name}"
    )
    checkpoint_save_path.parents[0].mkdir(parents=True)
    shutil.copyfile(checkpoint_load_path, checkpoint_save_path)


def compile_index_csv(
    images_load_path: pathlib.Path,
    DP_images_path: pathlib.Path,
    annotations: pd.DataFrame,
    object: str,
) -> pd.DataFrame:
    """Compiles index csv file (image metadata, channel image locations, genotype).
    Args:
        images_load_path (pathlib.Path): Path to load illuminated corrected images from 
        DP_images_path (pathlib.Path): Path to DP project images folder (DP_project/inputs/images)
        annotations (pd.DataFrame): NF1 data annotations metadata csv file
        object (str): Object to compile index csv for, either "nuc" (nucleus) or "cyto" (cytoplasm)
    Returns:
        pd.DataFrame: index csv dataframe
    """
    # Empty data frame for index to be appended to
    index_csv_data = []

    for image_paths in images_load_path.iterdir():
        # Skip over files without DAPI in image path name
        if "DAPI" not in image_paths.name:
            continue

        # Get image metadata
        plate = int(image_paths.name[3:5])
        well = image_paths.name[0:2]
        site = image_paths.name[8]

        # Get genotype value for images, assign plate and well columns from annotations for index
        image_annotations = annotations.loc[
            (plate == annotations["Plate"]) & (annotations["Well"] == well)
        ]
        genotype = image_annotations.iloc[0]["Genotype"]

        # Compile object index file data
        # Note: In the NF1 data, the "RNA" channel is actually the "Actin" channel, but wanted to follow the same naming as LUAD paper
        channels = ["DNA", "ER", "Actin"]

        file_data = {
            "Metadata_Plate": plate,
            "Metadata_Well": well,
            "Metadata_Site": site,
            "Plate_Map_Name": f"{plate}_{well}_{site}",
        }

        # For loop to go through all of the channels to get metadata from
        for index, channel in enumerate(channels):
            # Create channel path that increases by one for every consecutive channel portion of the image name
            # Count is set to one to only change the first instance that '_1_' occurs (only change channel not site)
            channel_path = pathlib.Path(
                str(image_paths).replace("_1_", f"_{index+1}_"), count=1
            )

            # Since the channel path will keep 'DAPI' for all images, these if statements will change the name to respective channel based on name
            if "01_2_" in str(channel_path):
                channel_path = pathlib.Path(str(channel_path).replace("DAPI", "GFP"))
            if "01_3_" in str(channel_path):
                channel_path = pathlib.Path(str(channel_path).replace("DAPI", "RFP"))
            # Save paths to each image into the index.csv under the correct column (within dictionary) with the name of the channel
            file_data[channel] = os.path.relpath(channel_path, DP_images_path)

        # Add Genotype and Genotype_Replicate (hard coded to 1 for NF1 data) with to file_data dictionary
        file_data["Genotype"] = genotype
        file_data["Genotype_Replicate"] = 1

        # Append all of the data into an index.csv file
        index_csv_data.append(file_data)

    return pd.DataFrame(index_csv_data)


def compile_training_locations(
    index_csv_path: pathlib.Path,
    segmentation_data_path: pathlib.Path,
    save_path: pathlib.Path,
    object: str,
):
    """Compile well-site-object.csv file with cell locations, saving to save_path/plate/well.
    Args:
        index_csv_path (pathlib.Path): Path to index.csv file for object (nuc or cyto) DeepProfiler project
        segmentation_data_path (pathlib.Path): Path to segmentation folder with .tsv locations files
        save_path (pathlib.Path): Path to save location files
        object (str): Object to find segmentation locations for, either "nuc" or "cyto"
    """
    # Reads in csv and iterate through the rows from the plate, well and site columns
    index_csv = pd.read_csv(index_csv_path)
    for index, row in index_csv.iterrows():
        plate = row["Metadata_Plate"]
        well = row["Metadata_Well"]
        site = row["Metadata_Site"]

        # Gets identifier string that matches identifier from segmented images tsvs
        identifier_details = row["DNA"].split("/")[-1].split("_")[0:4]
        identifier_well = identifier_details[0]
        identifier_site = identifier_details[3]
        identifier = f"{identifier_well}_{identifier_site}"

        # Note: The name is hard coded to "Nuclei.csv" due to how the pretrained model works. Even though it should be Cytoplasm for the cyto_project,
        # it has to be named "Nuclei" to prevent errors when running DeepProfiler (e.g saying no cells to profile when there are)
        locations_save_path = pathlib.Path(
            f"{save_path}/{plate}/{well}-{site}-Nuclei.csv"
        )

        # Skips a field if the locations have already been found
        if locations_save_path.is_file():
            print(f"{plate} + {identifier} already has locations compiled!")
        else:

            print(f"Compiling locations for {plate} + {identifier}")
            frame_segmentations_path = pathlib.Path(
                f"{segmentation_data_path}/{identifier}_{object}-segmented.tsv"
            )

            # Handle errors for issues like no locations file or no data within file
            try:
                frame_segmentations = pd.read_csv(
                    frame_segmentations_path, delimiter="\t"
                )
            except:
                print(f"No segmentation file for {frame_segmentations_path.name}")
                continue
            try:
                frame_segmentations = frame_segmentations[
                    ["Cell_ID", "Location_Center_X", "Location_Center_Y"]
                ]
            except KeyError:
                print(f"No segmentation data within {frame_segmentations_path}")
                continue

            # Note: As decribed above, even though in the cyto_project it is using Cytoplasm center coords, for DeepProfiler to work with the model, it must
            # be in this specific naming structure
            frame_segmentations = frame_segmentations.rename(
                columns={
                    "Location_Center_X": "Nuclei_Location_Center_X",
                    "Location_Center_Y": "Nuclei_Location_Center_Y",
                }
            )

            locations_save_path.parents[0].mkdir(parents=True, exist_ok=True)
            frame_segmentations.to_csv(locations_save_path, index=False)


def compile_project(
    project_path: pathlib.Path,
    checkpoint_name: str,
    annotations_path: pathlib.Path,
    images_load_path: pathlib.Path,
    segmentation_data_path: pathlib.Path,
    object: str,
):
    """Compile DP project for specified object of interest.
    Args:
        project_path (pathlib.Path): Path to compile DP project to for an object
        checkpoint_name (str): Name of checkpoint to use in DP project (must be located in DP_files/)
        annotations_path (pathlib.Path): Path to NF1 annotations data
        images_load_path (pathlib.Path): Path to load NF1 illumination corrected images to extract features from
        segmentation_data_path (pathlib.Path): Path to folder with segmentation tsv files 
        object (str): Object to compile project for, must be "nuc" or "cyto"
    """
    # Make project directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Copy necessary DP files from DP_files/ to DP project
    config_name = f"NF1_{object}_config.json"
    copy_DP_files(project_path, config_name, checkpoint_name)

    # Compile and save object index.csv file to DP project for object
    # Read in annotations file to use in function
    annotations = pd.read_csv(annotations_path)

    # Create path for index.csv file within the project path
    index_save_path = pathlib.Path(f"{project_path}/inputs/metadata/index.csv")
    index_save_path.parents[0].mkdir(parents=True, exist_ok=True)
    print("compiling index.csv file...")

    # Create path for the images in the DP project
    DP_images_path = pathlib.Path(f"{project_path}/inputs/images")

    # Run function to compile the index.csv
    index_csv = compile_index_csv(images_load_path, DP_images_path, annotations, object)
    index_csv.to_csv(index_save_path, index=False)
    print("index.csv file saved!")

    # Compile and save locations to DP project for specified object
    locations_save_path = pathlib.Path(f"{project_path}/inputs/locations/")
    print("Compiling locations!")
    compile_training_locations(
        index_save_path, segmentation_data_path, locations_save_path, object
    )
    print("Done compiling locations!")


def rename_cyto_locations(cyto_locations_path: pathlib.Path):
    """Rename the .csv files within directory from "Nuclei.csv" to "Cytoplasm.csv" to avoid confusion during downstream analysis. See Step 7 in the README
    for more information.

    Args:
        cyto_locations_path (pathlib.Path): Path to cyto_project directory (currently only set up to be one plate, so directory goes to the plate)
    """
    for location_files in cyto_locations_path.iterdir():
        new_cyto_location_files = str(location_files).replace("Nuclei", "Cytoplasm")
        Path(location_files).rename(Path(new_cyto_location_files))
