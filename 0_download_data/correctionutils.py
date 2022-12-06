import os

def run_cellprofiler(
    path_to_pipeline: str, path_to_output: str, path_to_images: str, output_folder_name : str
):
    """Profile batch with CellProfiler (runs segmentation and feature extraction) and rename the file after the run
    to the name of the plate

    Args:
        path_to_pipeline (str): path to the CellProfiler .cppipe file with the segmentation and feature measurement modules
        path_to_output (str): path to the output folder for the .sqlite file
        path_to_images (str): path to folder with IC images from specific plate
    """
    # run CellProfiler on a plate that has not been analyzed yet
    command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} -i {path_to_images}"
    os.system(command)
