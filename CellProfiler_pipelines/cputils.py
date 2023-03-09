"""
This collection of functions runs CellProfiler on the NF1 data for each plate and will rename the .sqlite outputed as the
the method used to process the data.
"""

import os
import pathlib


def rename_sqlite_file(sqlite_dir_path: pathlib.Path, method: str):
    """Rename the .sqlite file to be {method}.sqlite as to differentiate between the files

    Args:
        sqlite_dir_path (pathlib.Path): path to CellProfiler_output directory
        method (str): name of the method used that was run through CellProfiler (e.g., PyBaSiC IC and CellProfiler feature extraction, etc.)
    """
    try:
        # CellProfiler requires a name to be set in to pipeline, so regardless of plate or method, all sqlite files are outputed as "NF1_data.sqlite"
        sqlite_file_path = pathlib.Path(f"{sqlite_dir_path}/NF1_data.sqlite")

        new_file_name = str(sqlite_file_path).replace(
            sqlite_file_path.name, f"{method}.sqlite"
        )

        # change the file name in the directory
        pathlib.Path(sqlite_file_path).rename(pathlib.Path(new_file_name))
        print(f"The file is renamed to {pathlib.Path(new_file_name).name}!")

    except FileNotFoundError as e:
        print(
            f"The NF1_data.sqlite file is not found in directory. Either the pipeline wasn't ran properly or the file is already renamed.\n"
            f"{e}"
        )


def run_cellprofiler(
    path_to_pipeline: str, path_to_output: str, path_to_images: str, plugins_directory: str, method_name: str
):
    """Profile batch with CellProfiler (runs segmentation and feature extraction) and rename the file after the run
    to the name of the method

    Args:
        path_to_pipeline (str): path to the CellProfiler .cppipe file with the segmentation and feature measurement modules
        path_to_output (str): path to the output folder for the .sqlite file
        path_to_images (str): path to folder with IC images from specific plate
        plugins_directory (str) : path to plugins directory in the cloned CellProfiler repo (only works if CellProfiler is installed from source)
        method_name (str): string with method name
    """
    # runs through any files that are in the output path
    if any(
        files.name.startswith(method_name)
        for files in pathlib.Path(path_to_output).iterdir()
    ):
        print("This plate has already been analyzed!")
        return

    # if cellpose in not in the method name (e.g., Cellpose is not used for segmentation), then use the command without plugin directory
    if not 'cellpose' in method_name:
    # run CellProfiler on a plate that has not been analyzed yet
        command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} -i {path_to_images}"
        os.system(command)
    # if cellpose is in the method name, run the command with the plugins directory flag
    else:
        command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} -i {path_to_images} --plugins-directory {plugins_directory}"
        os.system(command)

    # rename the outputted .sqlite file to the
    rename_sqlite_file(sqlite_dir_path=pathlib.Path(path_to_output), method=method_name)
