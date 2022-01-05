library(grid)
library(xtable)

format_axis_labels <- function(a) {
  sapply(a, function(x) {if (x >= 1000000) {x = paste(x/1000000, "M", sep = "")}
    else if (x>=1000) {x = paste(x/1000, "K", sep = "")}
    else {x = x}
  })
}

interactions <- read.table("interactionplot.1.interaction")
interactions_stat <- interactions[, 1:7]
interactions_stat[, c(1, 4)] <- sapply(interactions_stat[, c(1, 4)], as.character)
interactions_stat[, c(2, 3, 5, 6, 7)] <- sapply(interactions_stat[, c(2, 3, 5, 6, 7)], as.numeric)
interactions_same_chr <- interactions_stat[which(interactions_stat[[1]] == interactions_stat[[4]]), ]
clusters <- interactions_same_chr

cyto <- read.table("interactionplot.1.cyto.txt", fill = T, header = F)
cyto <- cyto[nchar(as.character(cyto[[1]])) <= 5, ]
layout_nrow <- length(unique(cyto[[1]]))
peaks <- read.table("interactionplot.1.peak")
peaks[[4]] <- (peaks[[4]] - min(peaks[[4]]))/(max(peaks[[4]]) - min(peaks[[4]]))

source("interactionplot.1.Plotting_functions.R")
pdf("interactionplot.1.pdf", width = 9, height = 11)
plot_layout(layout_nrow * 3, 2, heights = unit(rep(c(1.3, 0.4, 1.3)/(layout_nrow * 3), layout_nrow), "npc"), widths = unit(c(0.1, 0.9), "npc"))
plot_intra_chr_interaction(clusters, cyto, peaks)
dev.off()

