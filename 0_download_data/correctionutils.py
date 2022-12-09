import os
import pathlib

def correct_images(
    path_to_pipeline: str, path_to_output: str, path_to_images: str, output_folder_name : str
):
    """Profile batch with CellProfiler (runs segmentation and feature extraction) and rename the file after the run
    to the name of the plate

    Parameters
    ----------
        path_to_pipeline (str): path to the CellProfiler .cppipe file with the segmentation and feature measurement modules
        path_to_output (str): path to the output folder for the .sqlite file
        path_to_images (str): path to folder with IC images from specific plate
    """
    # run CellProfiler on a plate that has not been analyzed yet
    command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} -i {path_to_images}"
    os.system(command)

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

    for images in path_to_images.iterdir():
        image_names = images.name.split("_")
        print(image_names)
