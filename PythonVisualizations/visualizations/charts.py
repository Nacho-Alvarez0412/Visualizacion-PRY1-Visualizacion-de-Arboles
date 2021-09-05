import plotly.graph_objects as go
import plotly.express as px
from visualizations.transformations import create_hierarchical_structure, create_section_hierarchical_structure, create_hs2_hierarchical_structure


def create_sunburst_chart(exports_data):
    """Creates a sunburst chart

    :param exports_data: A DataFrame that contains the data of the exportations
    :return: Sunburst chart with exportations data
    """
    fig = px.sunburst(exports_data,
            path=["Section", "HS2", "HS4"],
            values="Trade Value"
    )
    return fig


def create_icicle_chart(exports_data, orientation="h", chart_type="all"):
    """Creates an icicle chart

    :param exports_data: The data used to display in the chart
    :param orientation: The orientation of the chart
    :param chart_type: The type of the data used for the chart
    :return: An icicle chart with the exportation data
    """
    # Determine hierarchical structure
    icicle_data_structure = None
    if chart_type == "all":
        icicle_data_structure = create_hierarchical_structure(exports_data)
    elif chart_type == "section":
        icicle_data_structure = create_section_hierarchical_structure(exports_data)
    elif chart_type == "hs2":
        icicle_data_structure = create_hs2_hierarchical_structure(exports_data)
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