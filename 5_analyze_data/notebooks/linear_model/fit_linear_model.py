#!/usr/bin/env python
# coding: utf-8

# # Fit a linear model on cell morphology features
# 
# Our aim is to determine which features significantly contribute to NF1 genotype adjusted by cell count

# In[1]:


import pathlib
import pandas as pd

from sklearn.linear_model import LinearRegression

from pycytominer.cyto_utils import infer_cp_features


# In[2]:


# Define inputs and outputs
data_dir = pathlib.Path("..", "..", "..", "4_processing_features", "data")
cp_file = pathlib.Path(data_dir, "nf1_sc_norm_cellprofiler.csv.gz")

output_dir = pathlib.Path("results")
output_file = pathlib.Path(output_dir, "linear_model_cp_features.tsv")


# In[3]:


# Load data


cp_df = pd.read_csv(cp_file, index_col=0)

# Define CellProfiler features
cp_features = infer_cp_features(cp_df)

print(f"We are testing {len(cp_features)} CellProfiler features")
print(cp_df.shape)
cp_df.head()


# ## Fit linear model

# In[4]:


# Setup linear modeling framework
variables = ["Metadata_number_of_singlecells"]
X = cp_df.loc[:, variables]

# Add dummy matrix of categorical genotypes
genotype_x = pd.get_dummies(data=cp_df.Metadata_genotype)

X = pd.concat([X, genotype_x], axis=1)

print(X.shape)
X.head()


# In[5]:


# Fit linear model for each feature
lm_results = []
for cp_feature in cp_features:
    # Subset CP data to each individual feature (univariate test)
    cp_subset_df = cp_df.loc[:, cp_feature]

    # Fit linear model
    lm = LinearRegression(fit_intercept=True)
    lm_result = lm.fit(X=X, y=cp_subset_df)
    
    # Extract Beta coefficients
    # (contribution of feature to X covariates)
    coef = lm_result.coef_
    
    # Estimate fit (R^2)
    r2_score = lm.score(X=X, y=cp_subset_df)
    
    # Add results to a growing list
    lm_results.append([cp_feature, r2_score] + list(coef))

# Convert results to a pandas DataFrame
lm_results = pd.DataFrame(
    lm_results,
    columns=["feature", "r2_score", "cell_count_coef", "Null_coef", "WT_coef"]
)

# Output file
lm_results.to_csv(output_file, sep="\t", index=False)

print(lm_results.shape)
lm_results.head()


# In[6]:


# Small exploration visualization
lm_results.plot(x="cell_count_coef", y="WT_coef", kind="scatter")

