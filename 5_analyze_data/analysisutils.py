import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import rgb2hex
import seaborn as sns
import pandas as pd
import pathlib
import umap

# make random np operations reproducible
np.random.seed(0)


def split_data(pycytominer_output: pd.DataFrame):
    """
    split pycytominer output to metadata dataframe and np array of feature values
    Parameters
    ----------
    pycytominer_output : pd.DataFrame
        dataframe with pycytominer output
    Returns
    -------
    pd.Dataframe, np.ndarray
        metadata dataframe, feature values
    """
    # split metadata from features
    metadata_cols = [
        col_name
        for col_name in pycytominer_output.columns.tolist()
        if "Metadata" in col_name
    ]
    metadata_dataframe = pycytominer_output[metadata_cols]

    feature_cols = [
        col_name
        for col_name in pycytominer_output.columns.tolist()
        if "Metadata" not in col_name
    ]
    feature_data = pycytominer_output[feature_cols].values

    return metadata_dataframe, feature_data


def get_class_colors(classes_list: list, palette: str) -> dict:
    """
    get class colors dictionary from a class list
    Parameters
    ----------
    classes_list : list
        list of classes to get colors from
    palette : str
        seaborn palette name to get colors from
    Returns
    -------
    dict
        dictionary with class names as keys and hex color strings as values
    """

    class_colors = {}

    cmap = sns.color_palette(palette, len(classes_list))
    for index, class_name in enumerate(classes_list):
        class_colors[class_name] = rgb2hex(cmap[index])

    return class_colors


def show_1D_umap(
    feature_data: np.ndarray,
    metadata_series: pd.Series,
    class_colors: dict,
    save_path=None,
    point_size: int = 5,
    alpha: float = 1,
    show_plot: bool = True,
):
    """
    show (and save) 1D umap, colored by metadata
    classes not included in colored_classes will be colored gray
    Parameters
    ----------
    feature_data : np.ndarray
        data for features to plot
    metadata_series : pd.Series
        metadata used to color data
    class_colors : dict
        colors for classes, any classes not specified will be gray
    save_path : _type_, optional
        where to save umap, by default None, by default None
    point_size : int, optional
        size of umap points, by default 5
    alpha : float, optional
        opacity of umap points, by default 1
    show_plot : bool, optional
        display plot in notebook, by default True 
    """
    # create umap object for dimension reduction
    reducer = umap.UMAP(random_state=0, n_components=1)
    # Fit UMAP and extract latent vars
    embedding = pd.DataFrame(reducer.fit_transform(feature_data), columns=["UMAP1"])
    # add phenotypic class to embeddings
    embedding[metadata_series.name] = metadata_series.tolist()

    # create random y distribution to space out points
    y_distribution = np.random.rand(feature_data.shape[0])
    embedding["y_distribution"] = y_distribution.tolist()

    fig = plt.figure(figsize=(15, 15))
    ax = fig.gca()
    legend_elements = []

    # keep track of if "other" classes exist
    other_classes_exist = False

    # add each phenotypic class to 1d graph and legend
    for index, metadata_class in enumerate(
        embedding[metadata_series.name].unique().tolist()
    ):
        class_embedding = embedding.loc[
            embedding[metadata_series.name] == metadata_class
        ]
        x = class_embedding["UMAP1"]
        y = class_embedding["y_distribution"]

        # color by class or gray if it should not be colored
        if metadata_class in class_colors.keys():
            color = class_colors[metadata_class]
            legend_elements.append(
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    label=metadata_class,
                    markerfacecolor=color,
                    markersize=10,
                )
            )
        else:
            other_classes_exist = True
            color = "#808080"

        ax.scatter(x, y, c=color, marker="o", alpha=alpha, s=point_size)

    # add "other" to legend if there are "other" classes
    if other_classes_exist:
        legend_elements.append(
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Other",
                markerfacecolor=color,
                markersize=10,
            )
        )

    plt.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5))
    # Label axes, title
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("Random Distribution")
    ax.set_title("1 Dimensional UMAP")

    # save umap
    if not save_path == None:
        plt.savefig(save_path, bbox_inches="tight")

    # not not display plot in notebook
    if show_plot == False:
        plt.close()
    # if set to True, display the plot
    else:
        plt.show()

def show_2D_umap(
    feature_data: np.ndarray,
    metadata_series: pd.Series,
    class_colors: dict,
    save_path=None,
    point_size: int = 5,
    alpha: float = 1,
    show_plot: bool = True,
):
    """
    show (and save) 2D umap, colored by metadata
    classes not included in colored_classes will be colored gray
    Parameters
    ----------
    feature_data : np.ndarray
        data for features to plot
    metadata_series : pd.Series
        metadata used to color data
    class_colors : dict
        colors for classes, any classes not specified will be gray
    save_path : _type_, optional
        where to save umap, by default None, by default None
    point_size : int, optional
        size of umap points, by default 5
    alpha : float, optional
        opacity of umap points, by default 1
    show_plot : bool, optional
        display plot in notebook, by default True 
    """
    # create umap object for dimension reduction
    reducer = umap.UMAP(random_state=0, n_components=2)
    # Fit UMAP and extract latent vars
    embedding = pd.DataFrame(
        reducer.fit_transform(feature_data), columns=["UMAP1", "UMAP2"]
    )
    # add phenotypic class to embeddings
    embedding[metadata_series.name] = metadata_series.tolist()

    fig = plt.figure(figsize=(15, 15))
    ax = fig.gca()
    legend_elements = []

    # keep track of if "other" classes exist
    other_classes_exist = False

    # add each phenotypic class to 1d graph and legend
    for index, metadata_class in enumerate(
        embedding[metadata_series.name].unique().tolist()
    ):
        class_embedding = embedding.loc[
            embedding[metadata_series.name] == metadata_class
        ]
        x = class_embedding["UMAP1"]
        y = class_embedding["UMAP2"]

        # color by class or gray if it should not be colored
        if metadata_class in class_colors.keys():
            color = class_colors[metadata_class]
            legend_elements.append(
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    label=metadata_class,
                    markerfacecolor=color,
                    markersize=10,
                )
            )
        else:
            other_classes_exist = True
            color = "#808080"

        ax.scatter(x, y, c=color, marker="o", alpha=alpha, s=point_size)

    # add "other" to legend if there are "other" classes
    if other_classes_exist:
        legend_elements.append(
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Other",
                markerfacecolor=color,
                markersize=10,
            )
        )

    plt.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5))
    # Label axes, title
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title("2 Dimensional UMAP")

    # save umap
    if not save_path == None:
        plt.savefig(save_path, bbox_inches="tight")

    # not not display plot in notebook
    if show_plot == False:
        plt.close()
    # if set to True, display the plot
    else:
        plt.show()

def show_3D_umap(
    feature_data: np.ndarray,
    metadata_series: pd.Series,
    class_colors: dict,
    save_path=None,
    point_size: int = 5,
    alpha: float = 1,
    show_plot: bool = True,
):
    """
    show (and save) 3D umap, colored by metadata
    classes not included in colored_classes will be colored gray
    Parameters
    ----------
    feature_data : np.ndarray
        data for features to plot
    metadata_series : pd.Series
        metadata used to color data
    class_colors : dict
        colors for classes, any classes not specified will be gray
    save_path : _type_, optional
        where to save umap, by default None, by default None
    point_size : int, optional
        size of umap points, by default 5
    alpha : float, optional
        opacity of umap points, by default 1
    show_plot : bool, optional
        display plot in notebook, by default True 
    """
    # create umap object for dimension reduction
    reducer = umap.UMAP(random_state=0, n_components=3)
    # Fit UMAP and extract latent vars
    embedding = pd.DataFrame(
        reducer.fit_transform(feature_data), columns=["UMAP1", "UMAP2", "UMAP3"]
    )
    # add phenotypic class to embeddings
    embedding[metadata_series.name] = metadata_series.tolist()

    fig = plt.figure(figsize=(15, 15))
    ax = fig.gca(projection="3d")
    legend_elements = []

    # keep track of if "other" classes exist
    other_classes_exist = False

    # add each phenotypic class to 3d graph and legend
    for index, metadata_class in enumerate(
        embedding[metadata_series.name].unique().tolist()
    ):
        class_embedding = embedding.loc[
            embedding[metadata_series.name] == metadata_class
        ]
        x = class_embedding["UMAP1"]
        y = class_embedding["UMAP2"]
        z = class_embedding["UMAP3"]

        # color by class or gray if it should not be colored
        if metadata_class in class_colors.keys():
            color = class_colors[metadata_class]
            legend_elements.append(
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    label=metadata_class,
                    markerfacecolor=color,
                    markersize=10,
                )
            )
        else:
            other_classes_exist = True
            color = "#808080"

        ax.scatter(x, y, z, c=color, marker="o", alpha=alpha, s=point_size)

    # add "other" to legend if there are "other" classes
    if other_classes_exist:
        legend_elements.append(
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Other",
                markerfacecolor=color,
                markersize=10,
            )
        )

    plt.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5))
    # Label axes, title
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_zlabel("UMAP 3")
    ax.set_title("3 Dimensional UMAP")

    # save umap
    if not save_path == None:
        plt.savefig(save_path, bbox_inches="tight")

    # not not display plot in notebook
    if show_plot == False:
        plt.close()
    # if set to True, display the plot
    else:
        plt.show()

def get_2D_umap_embeddings(feature_data: np.ndarray, random_state: int = 0):
    """
    get 2D umap embeddings for numpy array as x and y vectors

    Parameters
    ----------
    feature_data : np.ndarray
        feature data to find embeddings for
    random_state : int, optional
        random state for umap embeddings, by default 0

    Returns
    -------
    np.ndarray, np.ndarray
        X data vector, y data vector
    """
    # create umap object for dimension reduction
    reducer = umap.UMAP(random_state=random_state, n_components=2)

    # Fit UMAP and extract latent vars 1-2
    embedding = reducer.fit_transform(feature_data)
    embedding = np.transpose(embedding)

    # convert to numpy arrays
    x_data = embedding[0]
    y_data = embedding[1]

    # convert the numpy arrays into pandas dataframes
    x_data_df = pd.DataFrame(x_data, columns=["UMAP1"])
    y_data_df = pd.DataFrame(y_data, columns=["UMAP2"])

    # create variable for the UMAP2 column
    UMAP2_column = y_data_df["UMAP2"]

    # add UMAP2 column to the x_data_df with the UMAP1 column
    embeddings = x_data_df.join(UMAP2_column)

    return embeddings

def merge_metadata_embeddings(
    metadata_dataframe: pd.DataFrame, embeddings: pd.DataFrame, save_path: pathlib.Path
):
    """
    merge metadata with UMAP embeddings into one dataframe

    Parameters
    ----------
    metadata_dataframe : pd.Dataframe
        metadata for the NF1 single cells
    embeddings : pd.Dataframe
        2D UMAP embeddings for the x,y coordinates for each single cell

    Returns
    -------
    pd.Dataframe
    """
    # reset index to remove the 'Metadata_WellRow' as the index then drop the index
    metadata_dataframe = metadata_dataframe.reset_index()
    metadata_dataframe = metadata_dataframe.reset_index(drop=True)

    # remove index from embeddings dataframe as well to prevent IndexError
    embeddings = embeddings.reset_index(drop=True)

    # put dataframes into list of where the columns should go
    dataframes = [metadata_dataframe, embeddings]

    # merge dataframes together and save as .csv file
    merged_dataframe = pd.concat(dataframes, axis=1)
    merged_dataframe.to_csv(save_path, index=False)

    return merged_dataframe

def show_2D_umap_from_embeddings(
    feature_data: np.ndarray,
    metadata_series: pd.Series,
    save_path=None,
    random_state: int = 0,
    point_size: int = 5,
    alpha: float = 1,
    palette: str = "bright",
):
    """
    show 2D umap from 2D UMAP embeddings, save if desired
    Parameters
    ----------
    x_data : np.ndarray
        vector with X coordinates
    y_data : np.ndarray
        vector with Y coordinates
    metadata_series : pd.Series
        metadata for how to color umap points
    save_path : pathlib.Path, optional
        path to save umap image, by default None
    point_size : int, optional
        size of umap points, by default 5
    alpha : float, optional
        opacity of umap points, by default 1
    palette : str, optional
        color palette used to color points, by default "bright"
    """

    # create umap object for dimension reduction
    reducer = umap.UMAP(random_state=random_state, n_components=2)

    # Fit UMAP and extract latent vars 1-2
    embedding = reducer.fit_transform(feature_data)
    embedding = np.transpose(embedding)

    # convert to numpy arrays
    x_data = embedding[0]
    y_data = embedding[1]

    plt.figure(figsize=(15, 12))

    # Produce scatterplot with umap data, using metadata to color points
    sns_plot = sns.scatterplot(
        palette=palette,
        x=x_data,
        y=y_data,
        hue=metadata_series.tolist(),
        alpha=alpha,
        linewidth=0,
        s=point_size,
    )
    # Adjust legend
    sns_plot.legend(
        loc="center left", bbox_to_anchor=(1, 0.5), title=metadata_series.name
    )
    # Label axes, title
    sns_plot.set_xlabel("UMAP 1")
    sns_plot.set_ylabel("UMAP 2")
    sns_plot.set_title("2 Dimensional UMAP")

    # save umap
    if not save_path == None:
        plt.savefig(save_path, bbox_inches="tight")
