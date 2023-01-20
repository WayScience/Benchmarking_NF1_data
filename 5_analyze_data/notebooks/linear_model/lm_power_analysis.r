library(pwr)
suppressPackageStartupMessages(library(dplyr))

output_file <- file.path("results", "power_analysis_cp_features_lm.tsv")

# Load data
lm_results_file <- file.path("results", "linear_model_cp_features.tsv")
lm_results_df <- readr::read_tsv(
    lm_results_file,
    col_types = readr::cols(.default="d", feature="c")
)

print(dim(lm_results_df))
head(lm_results_df)

# Load feature data (for calculating n)
data_dir <-file.path("..", "..", "..", "4_processing_features", "data")
cp_file <- file.path(data_dir, "nf1_sc_norm_cellprofiler.csv.gz")

cp_df <- readr::read_csv(
    cp_file,
    col_types = readr::cols(
        .default="d",
        Metadata_WellRow="c",
        Metadata_WellCol="c",
        Metadata_Well="c",
        Metadata_gene_name="c",
        Metadata_genotype="c"
    )
)

print(dim(cp_df))
head(cp_df, 3)

# Define constants for power analysis
n_conditions <- 2  # NF1 WT and Null
n_samples <- dim(cp_df)[1]

u <- n_conditions - 1
v <- n_samples - u - 1
sig_level <- 0.05 / dim(lm_results_df)[1]
power <- 0.8

print(c(u, v))
print(sig_level)

# Given all R2 values perform power analysis
all_power_results <- list()
for (cp_feature in lm_results_df$feature) {
    # Subset to the given feature lm results
    lm_result_subset_df <- lm_results_df %>%
        dplyr::filter(feature == !!cp_feature)
    
    # Pull out the estimated R2 value
    r2_val <- lm_result_subset_df %>% dplyr::pull(r2_score)
    
    # The power estimate is undefined for r2_val = 1, skip if so
    if (r2_val == 1) {
        all_power_results[[cp_feature]] <- c(cp_feature, u, v, sig_level, NULL, NULL)
        next
    }
    
    # Transform R2 score to F2 effect size
    f2_val <- r2_val / (1 - r2_val)
    
    # Calculate power, note that v contains an estimate of sample size
    power_result <- pwr.f2.test(u = u, v = NULL, f2 = f2_val, sig.level = sig_level, power = power)
    
    # Calculate required sample size from the v formula
    estimated_sample_size <- power_result$v + u + 1
    
    # Save results for future visualization
    all_power_results[[cp_feature]] <- c(cp_feature, u, v, sig_level, power, estimated_sample_size)
    
}

power_results_df <- do.call(rbind, all_power_results) %>% dplyr::as_tibble()

colnames(power_results_df) <- c("feature", "u", "v", "sig_level", "power", "estimated_sample_size")

# Output to file
power_results_df %>%
    readr::write_tsv(output_file)

print(dim(power_results_df))
head(power_results_df)
