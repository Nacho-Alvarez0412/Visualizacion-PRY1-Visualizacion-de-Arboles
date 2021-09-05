import plotly.graph_objects as go
from data_transformations import create_hierarchical_structure, create_section_hierarchical_structure, create_hs2_hierarchical_structure


def create_icicle_plot(exports_data, orientation="h"):
    """Creates an icicle plot with all of the sections

    :param exports_data: DataFrame used to create the icicle plot
    :param orientation: The orientation of the plot
    :return: The icicle plot figure object
    """
    icicle_data_structure = create_hierarchical_structure(exports_data)
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


def create_icicle_from_section(exports_data, orientation="h"):
    """Creates an icicle plot with a certain section

    :param exports_data: DataFrame used to create the icicle plot
    :param orientation: The orientation of the plot
    :return: The icicle plot figure object
    """
    icicle_data_structure = create_section_hierarchical_structure(exports_data)
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


def create_icicle_from_hs2(exportations_data, orientation="h"):
    """Creates an icicle plot with an specific hs2 and section

        :param exportations_data: DataFrame used to create the icicle plot
        :param orientation: The orientation of the plot
        :return: The icicle plot figure object
    """
    icicle_data_structure = create_hs2_hierarchical_structure(exportations_data)
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