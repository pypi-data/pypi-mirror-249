from anndata import AnnData, read_h5ad
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy
from distinctipy import get_colors, get_hex
from pandas.api.types import is_numeric_dtype
from typing import List, Optional
from .plotting_data import plot_defaults

class DimRedPlot:
    '''
    A class to present a dimension reduction plot based on an annotated data.

    Attributes:
    -----------
    data : pandas.DataFrame
        A pandas data frame containing coordinates and meta values to be used for colors
    meta_id: str 
        which cell meta feature to use for colors 
    cont_type: bool 
        if meta_id is continouos
    dimred_id: str
        which dimension reduction from the object to use
    components:
        which components of the dimension reduction to use
    cell_ids:
        cell ids from the annotated data        
    dimred_id: str
        dimension reduction to use for scatter plot
    dimred_labels: str 
        dimension reduction name to use for axis labels
    cont_color: str
        color gradient scale for continuous cell meta or gene expression
    meta_order: List[str]
        order of cell meta factors for categorical meta
    meta_colors: List[str]
        colors to use for categorical meta
    selected_barcodes: List[str]
        which data points to color
    title: str
        title of the plot
    pt_size: int
        size of points in scatter plot
    ticks_font_size: int
        size of tick labels on x and y axis
    width: int|float|str
        width of the plot
    height: int|float|str
        height of the plot
    axis_font_size: int
        font size of the axis labels
    labels_size: int
        font size of labels for categorical meta
    legend_size: int
        font size for legend
    title_size: int
        font size for the title
    
    Methods:
    --------
    render_to_widget(...)->FigureWidget:
        returns a plotly graph_objects.Figure that contains the scatter plot with the data and aesthetics
    '''
    
    def __init__(self, 
                 adata: AnnData, 
                 meta_id: str, 
                 dimred_id: str, 
                 cont_type:bool = None, 
                 use_raw:bool = False, 
                 components:List[int] = None, 
                 dimred_id_suffix:str = "", 
                 ignore_meta:bool = False) -> None:

        '''
        Parameters:
        -----------  
        adata: annotated data object the dimention reduction plot to be based on 
        meta_id: which obs meta feature or the gene expression to use for colors 
        dimred_id: dimension reduction to use for scatter plot
        cont_type: if meta_id is continouos. If not provided or None, this will be inferred using pandas function is_numeric_dtype
        use_raw: either to use raw gene expression or scaled
        components: which of the components of the dimension reduction to use. Default is first two
        dimred_id_suffix: if a suffix is added to dimred_id in the annotated data. For example "X_" if scanpy is used for preprocess
        ignore_meta: either to manually set the object as a gene expression plot. Otherwise, adata.obs columns will be checked first and then the gene names to find coloring meta variable

        Returns:
        --------
        None
        '''    
        self.dimred_id = dimred_id
        dimred_id = dimred_id_suffix + dimred_id
        components = components if components != None else [0,1]
        
        if dimred_id not in adata.obsm_keys():
            raise(ValueError("Given dimention reduction is not found in Annotated Data!"))
        if meta_id not in adata.var_names.to_list() + adata.obs.columns.to_list():
            raise(ValueError("Meta ID is not found in obs columns or gene names!"))
        if ignore_meta and meta_id not in adata.var_names.to_list():
            raise(ValueError("Ignore meta is set to True the but Meta ID variable is not found gene names!"))
        
        self.meta_id = meta_id
        self.cell_ids = adata.obs_names        
        self.data = pd.DataFrame(adata.obsm[dimred_id][:,components], index=adata.obsm.dim_names, columns=["X", "Y"])
        
        if ignore_meta or meta_id not in adata.obs.columns.to_list():
            self.cont_type = True
            if use_raw and scipy.sparse.issparse(adata.X):
                self.data["meta"] = pd.Series(np.array(adata[:,meta_id].raw.X.todense()).reshape(-1), index = adata.obs_names)
            elif use_raw:
                self.data["meta"] = pd.Series(np.array(adata[:,meta_id].raw.X).reshape(-1), index = adata.obs_names)
            elif scipy.sparse.issparse(adata.X):
                self.data["meta"] = pd.Series(np.array(adata[:,meta_id].X.todense()).reshape(-1), index = adata.obs_names)
            else:
                self.data["meta"] = pd.Series(np.array(adata[:,meta_id].X).reshape(-1), index = adata.obs_names)
        else:
            self.cont_type = cont_type if cont_type != None else is_numeric_dtype(adata.obs[meta_id])
            if self.cont_type:
                self.data["meta_vals"] = adata.obs[meta_id]
            else:
                self.data["meta_vals"] = adata.obs[meta_id].astype(str)

    def set_cont_color(self, cont_color:str):
        self.cont_color = cont_color
    
    def set_meta_order(self, meta_order):
        if len(meta_order) != len(self.data["meta_vals"].unique().to_list()):
            raise(ValueError("The length of the meta order list is not the same as the number of factors"))
        else:
            self.meta_order = meta_order
    
    def set_meta_colors(self, meta_colors):
        if len(meta_colors) != len(self.data["meta_vals"].unique().to_list()):
            raise(ValueError("The length of the meta colors list is not the same as the number of factors"))
        else:
            self.meta_colors = meta_colors
    
    def set_selected_barcodes(self, selected_barcodes):
        if any(selected_barcodes not in self.cell_ids):
            raise(ValueError("Some barcodes are not in the annotated data"))
        else:
            self.selected_barcodes = selected_barcodes
    def set_title(self, title):
        self.title = title
    
    def set_dimred_labels(self, dimred_labels):
        self.dimred_labels = dimred_labels

    def set_pt_size(self, pt_size):
        self.pt_size = pt_size
    
    def set_ticks_font_size(self, ticks_font_size):
        self.ticks_font_size = ticks_font_size
    
    def set_width(self, width):
        self.width = width
    
    def set_axis_font_size(self, axis_font_size):
        self.axis_font_size = axis_font_size

    def set_labels_size(self, labels_size):
        self.labels_size = labels_size

    def set_legend_size(self, legend_size):
        self.legend_size = legend_size
    
    def set_title_size(self, title_size):
        self.title_size = title_size

    
    def render(self,
                render_to:str = "widget",
                cont_color: str = None, 
                meta_order: List[str] = None, 
                meta_colors: List[str] = None,  
                selected_barcodes: List[str] = None, 
                title: str = None,
                dimred_labels: str = None,
                pt_size: int = None, 
                ticks_font_size: int = None, 
                width: int|float|str = None, 
                height: int|float|str = None, 
                axis_font_size: int = None, 
                labels_size: int = None, 
                legend_size: int = None,
                title_size: int = None):
        
        '''
        Returns the rendered figure containing the scatter plot corresponding of the object.
        Each  aesthetics parameter is applied using function parameters if not given -> object attributes if not set 
        -> plot_defaults

        Parameters:
        -----------  
        render_to: which format to render the plot. Options are "widget", "html", "json"
        cont_color: color gradient scale for continuous cell meta. Can be anything Plotly graph object accepts
        meta_order: order of cell meta feature categories. This determines the order traces are added to figure and may cause some points covering other. If not provided pandas unique tolist function will be used
        meta_colors: colors to use for categorical obs meta. If not provided it will be set randomly using distinctpy library
        selected_barcodes: which data points to color. Remaining data points will be drawn grey with 0.5 opacity 
        title: title for the plot
        dimred_labels: the label of the dimension reduction axes
        pt_size: size of points in scatter plot 
        ticks_font_size: size of tick labels on x and y axis
        width: width of the plot. Can be auto or any value Plotly graph objects accepts
        height: height of the plot. Can be auto or 'true_asp_ratio' or any value Plotly graph objects accepts. If set to true_asp_ratio, width must be explicit and height will be set using the range of x/y values
        axis_font_size: font size of the axis labels. If not provided or None, axis labels will be omitted 
        labels_size: font size of labels for categorical meta. If set to False, labels won't be drawn
        legend_size: font size for legend. If set to False, legend will be hidden.
        title_size: font size for title. If set to False, legend will be hidden.

        Returns:
        --------
        Plotly Graphical Object Figure object containing dimention reduction scatter plot in three dimension. 
        '''
        if cont_color == None:
            if hasattr(self, 'cont_color'):
                cont_color = self.cont_color
            else:
                cont_color = plot_defaults["cont_color"]
        
        if pt_size == None:
            if hasattr(self, 'pt_size'):
                pt_size = self.pt_size
            else:
                pt_size = plot_defaults["pt_size"]
        
        if ticks_font_size == None:
            if hasattr(self, 'ticks_font_size'):
                ticks_font_size = self.ticks_font_size
            else:
                ticks_font_size = plot_defaults["ticks_font_size"]

        if not self.cont_type and meta_order == None:
            if hasattr(self, "meta_order"):
                meta_order = self.meta_order
            elif "meta_order" in plot_defaults:
                meta_order = plot_defaults["meta_order"]
            else:
                meta_order = self.data["meta_vals"].unique().tolist()
        
        if not self.cont_type and meta_colors == None:
            if hasattr(self, "meta_colors"):
                meta_colors = self.meta_colors
            elif "meta_colors" in plot_defaults:
                meta_colors = plot_defaults["meta_colors"]
            else:
                meta_colors = [get_hex(c) for c in get_colors(len(self.data["meta_vals"].unique().tolist()))]
        
        if selected_barcodes == None:
            if hasattr(self, "selected_barcodes"):
                selected_barcodes = self.selected_barcodes
            elif "selected_barcodes" in plot_defaults:
                selected_barcodes = plot_defaults["selected_barcodes"]
            else:
                selected_barcodes = False
        
        if title == None:
            if hasattr(self, "title"):
                title = self.title
            else:
                title = self.meta_id
        
        if dimred_labels == None:
            if hasattr(self, "dimred_labels"):
                dimred_labels = self.dimred_labels
            elif "dimred_labels" in plot_defaults:
                dimred_labels = plot_defaults["dimred_labels"]
            else:
                dimred_labels = self.dimred_id
        
        
        if width == None:
            if hasattr(self, "width"):
                width = self.width
            elif "width" in plot_defaults:
                width = plot_defaults["plotly_width"]
            else:
                width = "auto"
        
        if height == None:
            if hasattr(self, "height"):
                height = self.height
            elif "height" in plot_defaults:
                height = plot_defaults["plotly_height"]
            else:
                height = "auto"

        if axis_font_size == None:
            if hasattr(self, "axis_font_size"):
                axis_font_size = self.axis_font_size
            elif "axis_font_size" in plot_defaults:
                axis_font_size = plot_defaults["axis_font_size"]
            else:
                axis_font_size = False
        
        if labels_size == None:
            if hasattr(self, "labels_size"):
                labels_size = self.labels_size
            elif "labels_size" in plot_defaults:
                labels_size = plot_defaults["labels_size"]
            else:
                labels_size = False
        
        if legend_size == None:
            if hasattr(self, "legend_size"):
                legend_size = self.legend_size
            elif "legend_size" in plot_defaults:
                legend_size = plot_defaults["legend_size"]
            else:
                legend_size = False

        if title_size == None:
            if hasattr(self, "title_size"):
                title_size = self.title_size
            elif "title_size" in plot_defaults:
                title_size = plot_defaults["title_size"]
            else:
                title_size = False

        
        # if data is subsetted add grey points otherwise create empty figure
        if selected_barcodes:
            plotting_data_removed = self.data.loc[~self.data.index.to_series().isin(selected_barcodes),:]
            plotting_data = self.data.loc[selected_barcodes,:]
            fig = go.Figure(go.Scatter(x = plotting_data_removed["X"],
                        y = plotting_data_removed["Y"], 
                        mode="markers+text",
                        marker={"color":"#808080",
                                "opacity": 0.5,
                                "size":pt_size}))
        else:
            plotting_data = self.data
            fig = go.Figure()
        
        # add selected cell to the plot
        if not self.cont_type:
            colors = {k:v for k,v in zip(meta_order, meta_colors)}
            for i, meta_category in enumerate(list(plotting_data.meta_vals.unique())):
                fig.add_trace(go.Scatter(x = plotting_data.loc[plotting_data.meta_vals==meta_category,"X"],
                    y = plotting_data.loc[plotting_data.meta_vals==meta_category,"Y"], 
                    mode="markers+text",
                    hovertemplate="<b>X: </b>%{x:.2f}<br><b>Y: </b>%{y:.2f}<br><b>Category: </b>"+str(meta_category)+"<extra></extra>",
                    marker={"size":pt_size, "color":colors[str(meta_category)]}, name=str(meta_category)))
        else:
            fig.add_trace(go.Scatter(x = plotting_data.X,
                    y = plotting_data.Y,
                    mode="markers+text",
                    showlegend=False,
                    hovertemplate="<b>X: </b>%{x:.2f}<br><b>Y: </b>%{y:.2f}<br><b>Value: </b>%{marker.color:.2f}<extra></extra>",
                    marker={"size":pt_size,
                            "color":plotting_data.meta_vals,
                            "cmin":plotting_data.meta_vals.min(),
                            "cmax":plotting_data.meta_vals.max(),
                            "colorscale":cont_color,
                            "showscale":True}))
        
        if labels_size and self.cont_type:
            plotting_data.groupby("val").apply(
            lambda x: fig.add_annotation(x=x.X.mean(), y=x.Y.mean(), text=x.name, showarrow=False,
                                            font=dict(size=labels_size)))

        # add default layout
        fig.update_layout(
            margin=dict(
                l=5,
                r=5,
                b=10,
                t=10,
                pad=4
            ),
            paper_bgcolor="LightSteelBlue",
            xaxis=dict(tickfont=dict(size=ticks_font_size)),
            yaxis=dict(tickfont=dict(size=ticks_font_size))
        )

        # set axis text size and legend text size
        if axis_font_size:
            fig.update_layout(
            xaxis_title = dimred_labels + " 1",
            yaxis_title = dimred_labels + " 2",
            font = {
                "size": axis_font_size
            })
            
        if not legend_size:
            fig.update_layout(
            showlegend=False,
        )
        else:
            fig.update_layout(
            showlegend=True,
            legend = {"font":{"size":legend_size}}
        )
        # set width and height of the plot
        fig.update_layout(autosize=width=="auto" or height=="auto")
        if height=="true_asp_ratio":
            fig.update_layout(
            width=width,
            height=width*(plotting_data.Y.max() - plotting_data.Y.min())/ (plotting_data.X.max() - plotting_data.X.min())
            )
        elif height != "auto":
            fig.update_layout(
            height=height
            )
        if width != "auto":
            fig.update_layout(
            width=width
            )
        
        match render_to:
            case "widget":
                return fig
            case "html":
                return fig.to_html()
            case "json":
                return fig.to_json()