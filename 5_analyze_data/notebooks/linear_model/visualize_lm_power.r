suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(patchwork))

output_power_figure <- file.path("figures", "power_analysis_cp_lm.png")
output_dp_power_figure <- file.path("figures", "power_analysis_dp_lm.png")

# Load linear modeling results
lm_results_file <- file.path("results", "linear_model_cp_features.tsv")
lm_results_df <- readr::read_tsv(
    lm_results_file,
    col_types = readr::cols(.default="d", feature="c")
)

# Load linear modeling power
lm_power_file <- file.path("results", "power_analysis_cp_features_lm.tsv")
lm_power_df <- readr::read_tsv(
    lm_power_file,
    col_types = readr::cols(.default="d", feature="c")
)

# Merge for visualization
lm_data_df <- lm_results_df %>%
    dplyr::left_join(lm_power_df, by = "feature") %>%
    dplyr::arrange(estimated_sample_size) %>%
    dplyr::filter(estimated_sample_size < 100000) %>%  # Remove extreme outliers
    dplyr::filter(!is.na(power))

print(dim(lm_data_df))
head(lm_data_df)

# Load feature data (for current n)
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

n_samples <- dim(cp_df)[1]

print(dim(cp_df))
head(cp_df, 3)

power_gg <- (
    ggplot(lm_data_df, aes(y = estimated_sample_size, x = abs(WT_coef)))
    + geom_point(aes(color = abs(cell_count_coef)), size = 0.8)
    + theme_bw()
    + xlab("WT genotype contribution\n(Absolute value LM beta coefficient)")
    + ylab("Sample size to acheive 80% power\nwith Bonferroni adjusted significance threshold")
    + ggtitle("Power analysis for CP features")
    + geom_hline(yintercept = n_samples, linetype = "dashed", color = "red")
    + scale_color_gradient(name = "Cell density\ncontribution", low = "black", high = "lightblue")
)

power_gg

power_zoom_gg <- (
    ggplot(
        lm_data_df %>% dplyr::filter(abs(WT_coef) > 0.2),
        aes(y = estimated_sample_size, x = abs(WT_coef))
    )
    + geom_point(aes(color = abs(cell_count_coef)), size = 0.8)
    + theme_bw()
    + geom_hline(yintercept = n_samples, linetype = "dashed", color = "red")
    + xlab("WT genotype contribution\n(Absolute value LM beta coefficient)")
    + ylab("Sample size to acheive 80% power\nwith Bonferroni adjusted significance threshold")
    + ggtitle("Power analysis for CP features (zoom)")
    + scale_color_gradient(name = "Cell density\ncontribution", low = "black", high = "lightblue")
)

power_zoom_gg

full_power_gg <- power_gg + power_zoom_gg
ggsave(output_power_figure, full_power_gg, dpi = 500, width = 13, height = 6)

# Load linear modeling results
lm_results_file <- file.path("results", "linear_model_dp_features.tsv")
lm_results_df <- readr::read_tsv(
    lm_results_file,
    col_types = readr::cols(.default="d", feature="c")
)

# Load linear modeling power
lm_power_file <- file.path("results", "power_analysis_dp_cyto_features_lm.tsv")
lm_power_df <- readr::read_tsv(
    lm_power_file,
    col_types = readr::cols(.default="d", feature="c")
)

# Merge for visualization
lm_data_df <- lm_results_df %>%
    dplyr::left_join(lm_power_df, by = "feature") %>%
    dplyr::arrange(estimated_sample_size) %>%
    dplyr::filter(estimated_sample_size < 100000) %>%  # Remove extreme outliers
    dplyr::filter(!is.na(power))

print(dim(lm_data_df))
head(lm_data_df)

# Load feature data (for calculating n)
data_dir <-file.path("..", "..", "..", "4_processing_features", "data")
dp_file <- file.path(data_dir, "nf1_sc_norm_deepprofiler_cyto.csv.gz")

dp_df <- readr::read_csv(
    dp_file,
    col_types = readr::cols(
        .default="d",
        Metadata_Plate="c",
        Metadata_Well="c",
        Metadata_Site="c",
        Metadata_Plate_Map_Name="c",
        Metadata_DNA="c",
        Metadata_ER="c",
        Metadata_Actin="c",
        Metadata_Genotype="c",
        Metadata_Genotype_Replicate="c",
        Metadata_Model="c"
    )
)

n_samples <- dim(dp_df)[1]

print(dim(dp_df))
head(dp_df, 3)

power_gg <- (
    ggplot(lm_data_df, aes(y = estimated_sample_size, x = abs(WT_coef)))
    + geom_point(aes(color = abs(cell_count_coef)), size = 0.8)
    + theme_bw()
    + xlab("WT genotype contribution\n(Absolute value LM beta coefficient)")
    + ylab("Sample size to acheive 80% power\nwith Bonferroni adjusted significance threshold")
    + ggtitle("Power analysis for DP Cyto features")
    + geom_hline(yintercept = n_samples, linetype = "dashed", color = "red")
    + scale_color_gradient(name = "Cell density\ncontribution", low = "black", high = "lightblue")
)

power_gg

power_zoom_gg <- (
    ggplot(
        lm_data_df %>% dplyr::filter(abs(WT_coef) > 0.2),
        aes(y = estimated_sample_size, x = abs(WT_coef))
    )
    + geom_point(aes(color = abs(cell_count_coef)), size = 0.8)
    + theme_bw()
    + geom_hline(yintercept = n_samples, linetype = "dashed", color = "red")
    + xlab("WT genotype contribution\n(Absolute value LM beta coefficient)")
    + ylab("Sample size to acheive 80% power\nwith Bonferroni adjusted significance threshold")
    + ggtitle("Power analysis for DP Cyto features (zoom)")
    + scale_color_gradient(name = "Cell density\ncontribution", low = "black", high = "lightblue")
)

power_zoom_gg

full_power_gg <- power_gg + power_zoom_gg
ggsave(output_dp_power_figure, full_power_gg, dpi = 500, width = 13, height = 6)
