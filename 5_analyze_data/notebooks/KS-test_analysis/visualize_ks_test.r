suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(dplyr))

output_fig_dir <- "figures"

ks_test_fig <- file.path(output_fig_dir, "ks_test_cp_genotype.png")
er_distrib_fig <- file.path(output_fig_dir, "top_er_feature_distrib.png")

# Load and process KS-test data
ks_file <- file.path("data", "nf1_kstest_two_sample_results.csv")
ks_df <- readr::read_csv(ks_file, col_types = readr::cols(.default="d", Features="c"))

# Create a new column for a directional ks-test statistic
# Arrange by statistic
# Split out components of feature name for visualization
ks_df <- ks_df %>%
    dplyr::mutate(signed_statistic = statistic * statistic_sign) %>%
    dplyr::arrange(desc(statistic)) %>%
    tidyr::separate(
        Features,
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
ks_df$channel_cleaned <-
    dplyr::recode(
        ks_df$channel_cleaned,
        "DAPI" = "nuclei",
        "RFP" = "actin",
        "GFP" = "ER",
        .default = "other",
        .missing="other"
    )

print(dim(ks_df))
head(ks_df, 10)

# Load feature data
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

# Determine a bonferroni adjusted alpha value threshold
alpha <- 0.05
bon_alpha <- alpha / dim(ks_df)[1]
bon_alpha

ks_test_gg <- (
    ggplot(ks_df, aes(x = signed_statistic, y = -log10(pvalue)))
    + geom_point(alpha = 0.5, aes(color=channel_cleaned))
    + geom_hline(yintercept=-log10(bon_alpha), linetype = "dashed", color = "red")
    + theme_bw()
    + xlab("KS Test Statistic")
    + ylab("-log10 p value")
    + ggtitle("How different are CellProfiler features\nbetween NF1 genotypes?")
    + guides(color = guide_legend(title = "Channel\n(if applicable)"))
)

ks_test_gg

# Output figure
ggsave(ks_test_fig, ks_test_gg, dpi = 500, height = 6, width = 6)

top_er_feature <- ks_df %>%
    dplyr::filter(channel_cleaned == "ER") %>%
    dplyr::select(Features)

top_er_feature <- head(top_er_feature, 1) %>% dplyr::pull(Features)
top_er_feature

top_er_feature_gg = (
    ggplot(cp_df, aes(x = .data[[top_er_feature]]))
    + geom_density(aes(fill = Metadata_genotype), alpha = 0.7)
    + theme_bw()
    + ylab("Density")
    + guides(fill = guide_legend(title = "Genotype"))
)

top_er_feature_gg

# Output figure
ggsave(er_distrib_fig, top_er_feature_gg, dpi = 500, height = 6, width = 6)
