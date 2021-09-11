import plotly.graph_objects as go
from visualizations.transformations import create_hierarchical_structure_without_root, create_hierarchical_structure, create_section_hierarchical_structure, create_hs2_hierarchical_structure


def create_sunburst_chart(exports_data, chart_type="all"):
    """Creates a sunburst chart

    :param exports_data: A DataFrame that contains the data of the exportations
    :param chart_type: The type of the data used for the chart
    :return: Sunburst chart with exportations data
    """
    sunburst_data_structure = None
    if chart_type == "all":
        sunburst_data_structure = create_hierarchical_structure_without_root(exports_data)
    elif chart_type == "section":
        sunburst_data_structure = create_section_hierarchical_structure(exports_data)
    elif chart_type == "hs2":
        sunburst_data_structure = create_hs2_hierarchical_structure(exports_data)
    fig = go.Figure(go.Sunburst(
        labels=sunburst_data_structure["elements"],
        parents=sunburst_data_structure["parents"],
        values=sunburst_data_structure["values"],
        hovertemplate="%{label}<br />Trade Value: $%{value:,f}<extra></extra>",
        branchvalues="total",
        marker_colors=sunburst_data_structure["colors"]
    ))
    fig.update_layout(margin=dict(t=15, l=0, r=0, b=15), title_text="Exportaciones de Costa Rica en el 2019",
                      height=900, title_yanchor="middle", title_xanchor="left")
    return fig


def create_icicle_chart(exports_data, orientation="h", chart_type="all"):
    """Creates an icicle chart

    :param exports_data: The data used to display in the chart
    :param orientation: The orientation of the chart
    :param chart_type: The type of the data used for the chart
    :return: An icicle chart with the exportation data
    """
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
        hovertemplate="%{label}<br />Trade Value: $%{value:,f}<extra></extra>",
        marker_colors=icicle_data_structure["colors"],
        tiling={"orientation": orientation}
    ))
    chart_width = 900
    chart_height = 500 if orientation == "v" else 1000
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=25), width=chart_width, height=chart_height)
    return fig