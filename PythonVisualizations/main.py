import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from visualizations.plots import create_icicle_plot


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

country_exports_data = pd.read_csv('_data/exports.csv')
# Create polots
left_right_icicle_plot = create_icicle_plot(country_exports_data)
top_down_icicle_plot = create_icicle_plot(country_exports_data, orientation="v")

app.layout = html.Div([
  # Header
  html.Header(className="main-header", children=[
    html.H1(children="Exportaciones de Costa Rica"),
    html.P(children="Curso: Visualización de Información")
  ]),
  # Body
  html.Div(className="container", children=[
    html.H2(children="Icicle plot de izquierda a derecha"),
    dcc.Graph(figure=left_right_icicle_plot),
    html.H2(children="Icicle plot de arriba hacia abajo"),
    dcc.Graph(figure=top_down_icicle_plot),
  ]),
  # Footer
  html.Footer(className="main-footer", children="Desarrollado por Ignacio Álvarez y Andrés Aguilar")
])

if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


