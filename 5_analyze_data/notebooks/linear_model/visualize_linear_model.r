suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(dplyr))

input_dir <- "results"
lm_file <- file.path(input_dir, "linear_model_cp_features.tsv")
lm_dp_file <- file.path(input_dir, "linear_model_dp_features.tsv")

output_fig_dir <- "figures"
lm_fig <- file.path(output_fig_dir, "linear_model_cp_features.png")
lm_dp_fig <- file.path(output_fig_dir, "linear_model_dp_features.png")

# Load and process linear model data
lm_df <- readr::read_tsv(
    lm_file, col_types = readr::cols(.default = "d", feature = "c")
)

# Arrange by absolute value coefficient
# Split out components of feature name for visualization
lm_df <- lm_df %>%
    dplyr::arrange(desc(abs(Null_coef))) %>%
    tidyr::separate(
        feature,
        into = c(
            "compartment",
            "feature_group",
            "measurement",
            "channel", 
            "parameter1", 
            "parameter2"
        ),
        sep = "_",
        remove = FALSE
    ) %>%
    dplyr::mutate(channel_cleaned = channel)

# Clean channel for visualization
lm_df$channel_cleaned <-
    dplyr::recode(
        lm_df$channel_cleaned,
        "DAPI" = "nuclei",
        "RFP" = "actin",
        "GFP" = "ER",
        .default = "other",
        .missing="other"
    )

print(dim(lm_df))
head(lm_df, 10)

lm_fig_gg <- (
    ggplot(lm_df, aes(x = cell_count_coef, y = WT_coef))
    + geom_point(aes(size = r2_score, color = channel_cleaned), alpha = 0.7)
    + geom_vline(xintercept = 0, linetype = "dashed", color = "red")
    + geom_density2d(color="black", show.legend = FALSE)
    + theme_bw()
    + guides(
        color = guide_legend(title = "Channel\n(if applicable)", order = 1),
        size = guide_legend(title = "R2 score")
    )
    + ylab("WT genotype contribution (LM beta coefficient)")
    + xlab("Cell count contribution (LM beta coefficient)")
    + ggtitle("How CellProfiler features contribute\nto NF1 genotype and cell density")
)

# Output figure
ggsave(lm_fig, lm_fig_gg, dpi = 500, height = 6, width = 6)

lm_fig_gg

# Load and process linear model data
lm_dp_df <- readr::read_tsv(
    lm_dp_file, col_types = readr::cols(.default = "d", feature = "c")
)

print(dim(lm_dp_df))
head(lm_dp_df, 10)

lm_dp_fig_gg <- (
    ggplot(lm_dp_df, aes(x = cell_count_coef, y = WT_coef))
    + geom_density_2d_filled(alpha = 0.5, show.legend = FALSE)
    + geom_point(aes(size = r2_score), alpha = 0.3)
    + geom_vline(xintercept = 0, linetype = "dashed", color = "red")
    + theme_bw()
    + guides(
        size = guide_legend(title = "R2 score")
    )
    + ylab("WT genotype contribution (LM beta coefficient)")
    + xlab("Cell count contribution (LM beta coefficient)")
    + ggtitle("How DeepProfiler features contribute\nto NF1 genotype and cell density")
)

# Output figure
ggsave(lm_dp_fig, lm_dp_fig_gg, dpi = 500, height = 6, width = 6)

lm_dp_fig_gg
