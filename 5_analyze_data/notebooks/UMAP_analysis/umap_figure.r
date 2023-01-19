suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(dplyr))

# Set paths
umap_dir <- file.path("..", "..", "data")
umap_cp_file <- file.path(umap_dir, "norm_fs_embeddings_cp.csv.gz")
umap_dp_file <- file.path(umap_dir, "norm_fs_embeddings_dp_nuc.csv.gz")

output_fig_dir <- "figures"

umap_cp_fig <- file.path(output_fig_dir, "umap_cp.png")
umap_dp_fig <- file.path(output_fig_dir, "umap_dp.png")

# Load data
umap_cp_df <- readr::read_csv(
    umap_cp_file,
    col_types = readr::cols(
        .default = "d",
        Metadata_Well = "c",
        Metadata_WellRow = "c",
        Metadata_gene_name = "c",
        Metadata_genotype = "c"
    )
)

print(dim(umap_cp_df))
head(umap_cp_df, 3)

umap_cp_gg <- (
    ggplot(umap_cp_df, aes(x = UMAP1, y = UMAP2))
    + geom_point(
        aes(
            color = Metadata_number_of_singlecells,
            shape = Metadata_genotype
        )
    )
    + scale_shape_manual(name = "Genotype", values = c(3, 1))
    + scale_color_gradient(name = "Cell count", low = "green", high = "blue")
    + theme_bw()
)

umap_cp_gg

# Output figure
ggsave(umap_cp_fig, umap_cp_gg, dpi = 500, height = 6, width = 6)

# Load data
umap_dp_df <- readr::read_csv(
    umap_dp_file,
    col_types = readr::cols(
        .default = "d",
        Metadata_Well = "c",
        Metadata_Genotype = "c",
        Metadata_Genotype_Replicate = "c",
        Metadata_Model = "c",
        Metadata_Plate_Map_Name = "c",
        Metadata_Actin = "c",
        Metadata_DNA = "c",
        Metadata_ER = "c"
    )
)

print(dim(umap_dp_df))
head(umap_dp_df, 3)

umap_dp_gg <- (
    ggplot(umap_dp_df, aes(x = UMAP1, y = UMAP2))
    + geom_point(
        aes(
            color = Metadata_number_of_singlecells,
            shape = Metadata_Genotype
        )
    )
    + scale_shape_manual(name = "Genotype", values = c(3, 1))
    + scale_color_gradient(name = "Cell count", low = "green", high = "blue")
    + theme_bw()
)

umap_dp_gg

# Output figure
ggsave(umap_dp_fig, umap_dp_gg, dpi = 500, height = 6, width = 6)
