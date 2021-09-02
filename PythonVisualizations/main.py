import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from visualizations.plots import create_icicle_plot


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

country_exports_data = pd.read_csv('_data/test.csv')
# Create polots
left_right_icicle_plot = create_icicle_plot(country_exports_data)
top_down_icicle_plot = create_icicle_plot(country_exports_data, orientation="v")

app.layout = html.Div([
  html.H1(children="Hello World"),
  dcc.Graph(figure=left_right_icicle_plot),
  dcc.Graph(figure=top_down_icicle_plot),
])

if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


