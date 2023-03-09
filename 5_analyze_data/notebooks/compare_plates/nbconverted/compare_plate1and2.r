suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))

# Set file paths
coef_dir <- file.path("..", "linear_model", "results")
plate_1_file <- file.path(coef_dir, "Plate1", "linear_model_all_cp_features.tsv")
plate_2_file <- file.path(coef_dir, "Plate2", "linear_model_all_cp_features.tsv")

output_file <- file.path("figures", "plate1_vs_2_coefficients.png")

# Load coefficients
plate_1_df <- readr::read_tsv(
    plate_1_file, col_types=readr::cols(.default = "d", feature="c")
)

# Recode column names
colnames(plate_1_df)[seq(2, ncol(plate_1_df))] <- (
    paste0(colnames(plate_1_df)[seq(2, ncol(plate_1_df))], "_plate1")
)

plate_2_df <- readr::read_tsv(
    plate_2_file, col_types=readr::cols(.default = "d", feature="c")
)

colnames(plate_2_df)[seq(2, ncol(plate_2_df))] <- (
    paste0(colnames(plate_2_df)[seq(2, ncol(plate_2_df))], "_plate2")
)

plate_df <- plate_1_df %>%
    dplyr::full_join(plate_2_df, by = "feature") %>%
    dplyr::mutate(mean_r2 = (r2_score_plate1 + r2_score_plate2) / 2) %>%
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
plate_df$channel_cleaned <-
    dplyr::recode(
        plate_df$channel_cleaned,
        "DAPI" = "nuclei",
        "RFP" = "actin",
        "GFP" = "ER",
        .default = "other",
        .missing="other"
    )

print(dim(plate_df))
head(plate_df, 3)

cor_result <- cor.test(
    plate_df$Null_coef_plate1,
    plate_df$Null_coef_plate2,
    method = "pearson"
)
cor_result

plot_title <- paste0(
    "NF1 genotype differences are correlated across plates\n(r = ",
    round(cor_result$estimate, 2),
    ", p = ",
    format(cor_result$p.value, scientific = TRUE, digits = 2),
    ")"
)

coef_fig <- (
    ggplot(plate_df, aes(x = Null_coef_plate1, y = Null_coef_plate2))
    + geom_point(aes(size = mean_r2, color = channel_cleaned), alpha = 0.7)
    + theme_bw()
    + coord_fixed()
    + geom_vline(xintercept=0, linetype="dashed", color="blue")
    + geom_hline(yintercept=0, linetype="dashed", color="blue")
    + ylab("Null genotype contribution (LM beta coefficient)\nPlate 2")
    + xlab("Null genotype contribution (LM beta coefficient)\nPlate 1")
    + ggtitle(plot_title)
    + guides(
        color = guide_legend(title = "Channel\n(if applicable)", order = 1),
        size = guide_legend(title = "Average\nR2 score")
    )
)

# Output figure
ggsave(output_file, coef_fig, dpi = 500, height = 7, width = 8)

coef_fig
