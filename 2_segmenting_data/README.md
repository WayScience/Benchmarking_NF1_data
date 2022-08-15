# Segment Schwann Cells from NF1 Data

In this module, I present the pipeline for segmenting nuclei and cytoplasm from the NF1 pilot data.

### Segmentation

The method used for segmentation for both the nuclei and cytoplasm is an algorithm called [CellPose](https://doi.org/10.1038/s41592-020-01018-x). Through the python implementation of this method, this pipeline can be reproducible and is easy to manipulate for various datasets.

### Nuclei Segmentation

After experimenting with the various parameters in CellPose on all of the pilot NF1 DAPI (nuclei) channel images, I settled on the following parameters for CellPose nuclei segmentation:
- `model_type : "cyto"` This parameter sets the model from CellPose to be used as the cytoplasm model, which I found segments nuclei better than the established nucleus model. 
More information about CellPose models can be found at https://cellpose.readthedocs.io/en/latest/models.html.
- `channels : [0,0]` This parameter sets the channels to be used by the model to segment, which in the case of nuclei, we do not ned to set channels because the images are greyscale.
- `diameter : 50` This parameter sets the cell diameter of the cells within the image to a value, which can be calculated using the `calculate` button. 
I found that the segmentation worked better when the diameter was established with a set value. 
- `flow_threshold : 0` This paramenter decreases the maximum allowed error of the flows for each mask (default is `flow_threshold : 0.4`).
- `remove_edge_masks : True` This parameter removes any masks from CellPose that are touching an edge of the image.

### Cytoplasm Segmentation

After experimenting with the various parameters in CellPose on all of the pilot NF1 DAPI (RFP) channel images, we settled on the following parameters for CellPose cytoplasm segmentation:
- `model_type : "cyto2"` This parameter sets the model from CellPose to be used as the cytoplasm 2 model, which I found segments cytoplasm better than the other models.
- `channels : [1,3]` This parameter sets the channels to be used by the model to segment the cytoplasm of the cells using the nuclei as the base (1: blue) and the RFP channel as the channel to be segmented (3: red).
Since CellPose struggled with segmenting cytoplasm using only the RFP channel, I use a function to overlay nuclei, ER, and RNA channels into one image from each well and site called `overlay_channels()` in [segmentation_utils.py](segmentation_utils.py).
ER channel is not used by CellPose during segmentation as CellPose can only use 2 channels, one as a base and one to segment.

**Note:** The channel numbers 1,3 correspond to the CellPose colors red and blue respectively.
The `overlay()` function makes RNA the red channel of the image and DNA the blue channel of the image.
Thus, `channels : [1,3]` has CellPose segment the RNA channel using the DNA channel as its base.

- `diameter : 155` This parameter sets the cell diameter of the cells within the image to a value, which can be calculated using the `calculate` button. 
I found that the segmentation worked better when the diameter was established with a set value.
- `flow_threshold : 0.4` This paramenter decreases the maximum allowed error of the flows for each mask (default is `flow_threshold : 0.4`).
- `remove_edge_masks : True` This parameter removes any masks from CellPose that are touching an edge of the image.
