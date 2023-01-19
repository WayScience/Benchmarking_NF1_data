suppressPackageStartupMessages(library(ComplexHeatmap))
suppressPackageStartupMessages(library(dplyr))

# Set paths and constants
input_data_dir <- file.path("..", "..", "..", "4_processing_features", "data")
output_figure_dir <- "figures"

cp_heatmap_file <- file.path(output_figure_dir, "cp_complex_heatmap.pdf")
dp_heatmap_file <- file.path(output_figure_dir, "dp_complex_heatmap.pdf")

# Set heatmap colors
well_cols = c(
    "C6" = "#E1DAAE",
    "C7" = "#FF934F",
    "D6" = "#CC2D35",
    "D7" = "#058ED9",
    "E6" = "#848FA2",
    "E7" = "#2D3142",
    "F6" = "#FFC857",
    "F7" = "#5f7a12"
)
genotype_cols = c(
    "Null" = "#785EF0",
    "WT" = "#DC267F"
)

# Load data
cp_file <- file.path(input_data_dir, "nf1_sc_norm_fs_cellprofiler.csv.gz")

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
) %>% dplyr::select(-...1)  # Drop index col

print(dim(cp_df))
head(cp_df, 3)

# Split metadata and feature data
cp_metadata_df <- cp_df %>% dplyr::select(tidyr::starts_with("Metadata"))
cp_meta_cols <- colnames(cp_metadata_df)
cp_df <- cp_df %>% dplyr::select(-!!cp_meta_cols)

# Calculate correlation matrix from feature data
cp_cor_matrix <- t(cp_df) %>% cor()

print(dim(cp_cor_matrix))
head(cp_cor_matrix, 3)

ht <- Heatmap(
    cp_cor_matrix,
    name = "Pearson\nCorrelation",
    column_dend_side = "top",
    
    clustering_method_columns = "average",
    clustering_method_rows = "average",
    
    top_annotation = HeatmapAnnotation(
        Genotype = cp_metadata_df$Metadata_genotype,
        CellCount = anno_barplot(
            cp_metadata_df$Metadata_number_of_singlecells,
            height = unit(1, "cm")
        ),
        Well = cp_metadata_df$Metadata_Well,
        
        col = list(
            Genotype = genotype_cols,
            Well = well_cols
        )
    )
)

draw(ht)

# Save heatmap to file
pdf(cp_heatmap_file)
draw(ht)
dev.off()

# Load data
dp_file <- file.path(input_data_dir, "nf1_sc_norm_fs_deepprofiler_nuc.csv.gz")

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

print(dim(dp_df))
head(dp_df, 3)

# Split metadata and feature data
dp_metadata_df <- dp_df %>% dplyr::select(tidyr::starts_with("Metadata"))
dp_meta_cols <- colnames(dp_metadata_df)
dp_meta_cols <- c(dp_meta_cols, c("Location_Center_X", "Location_Center_Y"))

dp_df <- dp_df %>% dplyr::select(-!!dp_meta_cols)

# Calculate number of single cells per well in DP data
dp_metadata_df <- dp_metadata_df %>%
    dplyr::group_by(Metadata_Well) %>%
    dplyr::add_tally(name = "Metadata_cell_count")

# Calculate correlation matrix from feature data
dp_cor_matrix <- t(dp_df) %>% cor()

print(dim(dp_cor_matrix))
head(dp_cor_matrix, 3)

ht <- Heatmap(
    dp_cor_matrix,
    name = "Pearson\nCorrelation",
    column_dend_side = "top",
    
    clustering_method_columns = "average",
    clustering_method_rows = "average",
    
    top_annotation = HeatmapAnnotation(
        Genotype = dp_metadata_df$Metadata_Genotype,
        CellCount = anno_barplot(
            dp_metadata_df$Metadata_cell_count,
            height = unit(1, "cm")
        ),
        Well = dp_metadata_df$Metadata_Well,
        
        col = list(
            Genotype = genotype_cols,
            Well = well_cols
        )
    )
)

draw(ht)

# Save heatmap to file
pdf(dp_heatmap_file)
draw(ht)
dev.off()
