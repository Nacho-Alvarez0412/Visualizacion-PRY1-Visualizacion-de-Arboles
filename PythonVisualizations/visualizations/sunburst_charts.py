import plotly.express as px


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