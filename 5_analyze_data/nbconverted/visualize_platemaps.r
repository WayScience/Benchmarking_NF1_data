suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(platetools))

# Set output files
output_dir <- "platemap_figures"

input_platemap_dir <- file.path("..", "3_extracting_features", "metadata")

platemap_file <- file.path(input_platemap_dir, "NF1_annotations.csv")

platemap_df <- readr::read_csv(
    platemap_file,
    col_types = readr::cols(
        .default = "c"
    )
)

print(dim(platemap_df))
head(platemap_df, 3)

plate_replicate_gg <- (
    platetools::raw_map(
        data = platemap_df$Genotype,
        well = platemap_df$Well,
        plate = 96,
        size = 8
    )
    + scale_fill_discrete(name="Genotype")
)

output_fig_genotype <- file.path(output_dir, "genotype_platemap.png")

ggsave(
    output_fig_genotype,
    plate_replicate_gg,
    dpi = 500,
    height = 3.5,
    width = 6
)

plate_replicate_gg
