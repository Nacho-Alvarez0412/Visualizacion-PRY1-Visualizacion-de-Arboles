import dash_core_components as dcc
import dash_html_components as html
from visualizations.icicle_plots import create_icicle_plot
from visualizations.sunburst_charts import create_sunburst_chart


def create_main_layout(exportations_data):
    """Creates the main layout for the application

    :param exportations_data: The DataFrame used to display in the visualizations
    :return: The website main layout
    """
    # Create data visualizations
    sunburst_chart = create_sunburst_chart(exportations_data)
    left_right_icicle_plot = create_icicle_plot(exportations_data)
    top_down_icicle_plot = create_icicle_plot(exportations_data, orientation="v")

    product_sections = list(exportations_data["Section"].unique())

    main_layout = html.Div([
        # Header
        html.Header(className="main-header", children=[
            html.H1(children="Exportaciones de Costa Rica"),
            html.P(children="Curso: Visualización de Información")
        ]),
        # Body
        html.Div(className="container", children=[
            # Sunburst chart
            html.H2(children="Sunburst chart"),
            dcc.Graph(figure=sunburst_chart),
            # Left right icicle plot
            html.H2(children="Icicle plot de izquierda a derecha"),
            # Interactions
            html.Div(className="filter-options", children=[
                html.Label(["Selected section",
                            dcc.Dropdown(id="section-dropdown",
                                         options=[{"label": i, "value": i} for i in product_sections],
                            ),
                ]),
                html.Label(["Selected hs2",
                            dcc.Dropdown(id="hs2-dropdown",
                                         options=[],
                            ),
                ]),
            ]),
            # Plot
            dcc.Graph(id="left-right-icicle", figure=left_right_icicle_plot),
            # Top down icicle plot
            html.H2(children="Icicle plot de arriba hacia abajo"),
            # Plot
            dcc.Graph(figure=top_down_icicle_plot),
        ]),
        # Footer
        html.Footer(className="main-footer", children="Desarrollado por Ignacio Álvarez y Andrés Aguilar")
    ])

    return main_layout