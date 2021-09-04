import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from visualizations.plots import create_icicle_plot


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

country_exports_data = pd.read_csv('_data/exports.csv')

# Create polots
left_right_icicle_plot = create_icicle_plot(country_exports_data)
top_down_icicle_plot = create_icicle_plot(country_exports_data, orientation="v")

# TODO: Create dropdown menu for section
product_sections = list(country_exports_data["Section"].unique())
# TODO: Create dropdown menu for the section groups


app.layout = html.Div([
  # Header
  html.Header(className="main-header", children=[
    html.H1(children="Exportaciones de Costa Rica"),
    html.P(children="Curso: Visualización de Información")
  ]),
  # Body
  html.Div(className="container", children=[
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
    dcc.Graph(figure=left_right_icicle_plot),
    # Top down icicle plot
    html.H2(children="Icicle plot de arriba hacia abajo"),
    # Plot
    dcc.Graph(figure=top_down_icicle_plot),
  ]),
  # Footer
  html.Footer(className="main-footer", children="Desarrollado por Ignacio Álvarez y Andrés Aguilar")
])

@app.callback(
    Output("hs2-dropdown", "options"),
    Input("section-dropdown", "value")
)
def on_section_selected(selected_section):
    # Get hs2 groups by section name
    # TODO: Implement updates for icicle plot
    hs2_groups = country_exports_data[country_exports_data["Section"] == selected_section]["HS2"].unique()
    return [{"label": i, "value": i}  for i in list(hs2_groups)]



if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


