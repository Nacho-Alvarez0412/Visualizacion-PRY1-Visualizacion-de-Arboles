from data_transformation import create_hierarchical_structure
import plotly.graph_objects as go


def create_icicle_plot(exports_data, orientation="h"):
    """Creates an icicle plot from left to right

    :param exports_data: DataFrame used to create the icicle plot
    :param orientation: The orientation of the plot
    :return: The icicle plot figure object
    """
    icicle_data_structure = create_hierarchical_structure(exports_data)
    # Create plot
    fig = go.Figure(go.Icicle(
        labels=icicle_data_structure["elements"],
        parents=icicle_data_structure["parents"],
        values=icicle_data_structure["values"],
        branchvalues="total",
        root_color="lightgrey",
        tiling={"orientation": orientation}
    ))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig