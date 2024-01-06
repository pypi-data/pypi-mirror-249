import anndata
from sclive.plotting.DimRedPlot import DimRedPlot

adata  = anndata.read_h5ad("tests/pbmc.h5ad")
fig = DimRedPlot(adata, "leiden", "umap", dimred_id_suffix = "X_")
print(fig.render("widget"))