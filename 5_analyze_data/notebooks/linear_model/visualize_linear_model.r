suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(dplyr))

output_fig_dir <- "figures"

lm_fig <- file.path(output_fig_dir, "linear_model_cp_features.png")

# Load and process linear model data
lm_file <- file.path("results", "linear_model_cp_features.tsv")
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

(
    ggplot(lm_df, aes(x = cell_count_coef, y = abs(WT_coef)))
    + geom_point(aes(size = r2_score, color = channel_cleaned))
    + geom_vline(xintercept = 0, linetype = "dashed", color = "red")
    + geom_density2d(color="black", show.legend = FALSE)
    + theme_bw()
    + guides(
        color = guide_legend(title = "Channel\n(if applicable)", order = 1),
        size = guide_legend(title = "R2 score")
    )
    + ylab("Genotype contribution")
    + xlab("Cell count contribution")
    + ggtitle("How features contribute to NF1 genotype and cell density")
)
