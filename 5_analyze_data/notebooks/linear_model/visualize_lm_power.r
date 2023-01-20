suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(patchwork))

output_power_figure <- file.path("figures", "power_analysis_cp_lm.png")

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
    dplyr::filter(estimated_sample_size < 100000) %>%  # Remove extreme outlier
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
    + scale_color_gradient(name = "Cell density\ncontribution", low = "black", high = "lightblue")
)

power_zoom_gg

full_power_gg <- power_gg + power_zoom_gg
ggsave(output_power_figure, full_power_gg, dpi = 500, width = 13, height = 6)
