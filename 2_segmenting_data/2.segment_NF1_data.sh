
#!/bin/bash
jupyter nbconvert --to python Segmentation_Pipeline.ipynb
python Segmentation_Pipeline.py
