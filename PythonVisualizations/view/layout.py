import dash_core_components as dcc
import dash_html_components as html
from visualizations.charts import create_sunburst_chart, create_icicle_chart


def create_main_layout(exportations_data):
    """Creates the main layout for the application

    :param exportations_data: The DataFrame used to display in the visualizations
    :return: The website main layout
    """
    # Create data visualizations
    sunburst_chart = create_sunburst_chart(exportations_data)
    left_right_icicle_plot = create_icicle_chart(exportations_data)
    top_down_icicle_plot = create_icicle_chart(exportations_data, orientation="v")

    product_sections = list(exportations_data["Section"].unique())

    main_layout = html.Div([
        # Header
        html.Header(className="main-header", children=[
            html.Div(className="container", children=[
                html.H1(children="Exportaciones de Costa Rica"),
                html.P(children="Visualización de Información")
            ])
        ]),
        # Body
        html.Div(className="container", children=[
            # Sunburst chart
            html.H2(children="Sunburst chart"),
            html.Div(className="filter-options", children=[
                html.Label(["Selected section",
                            dcc.Dropdown(id="sunburst-section-dropdown",
                                         options=[{"label": i, "value": i} for i in product_sections],
                                         ),
                            ]),
                html.Label(["Selected hs2",
                            dcc.Dropdown(id="sunburst-hs2-dropdown",
                                         options=[],
                                         ),
                            ]),
            ]),
            dcc.Graph(figure=sunburst_chart, id="sunburst-chart"),
            # Left right icicle plot
            html.H2(children="Icicle plot de izquierda a derecha"),
            # Interactions
            html.Div(className="filter-options", children=[
                html.Label(["Selected section",
                            dcc.Dropdown(id="horizontal-icicle-section-dropdown",
                                         options=[{"label": i, "value": i} for i in product_sections],
                            ),
                ]),
                html.Label(["Selected hs2",
                            dcc.Dropdown(id="horizontal-icicle-hs2-dropdown",
                                         options=[],
                            ),
                ]),
            ]),
            # Plot
            dcc.Graph(id="left-right-icicle", figure=left_right_icicle_plot),
            # Top down icicle plot
            html.H2(children="Icicle plot de arriba hacia abajo"),
            html.Div(className="filter-options", children=[
                html.Label(["Selected section",
                            dcc.Dropdown(id="vertical-icicle-section-dropdown",
                                         options=[{"label": i, "value": i} for i in product_sections],
                                         ),
                            ]),
                html.Label(["Selected hs2",
                            dcc.Dropdown(id="vertical-icicle-hs2-dropdown",
                                         options=[],
                                         ),
                            ]),
            ]),
            # Plot
            dcc.Graph(id="vertical-icicle", figure=top_down_icicle_plot),
        ]),
        # Footer
        html.Footer(className="main-footer", children="Desarrollado por Ignacio Álvarez y Andrés Aguilar")
    ])

    return main_layout