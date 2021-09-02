import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from data_transformation import create_hierarchical_structure
from visualizations.plots import create_left_right_icicle_plot, create_top_down_icicle_plot
from visualizations.trees import create_radial_tree


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

# Create icicle plots
country_exports_data = pd.read_csv('_data/exports.csv')
icicle_hierarchical_structure = create_hierarchical_structure(country_exports_data)
# TODO: Display top-down icicle plot
# TODO: Display left-right icicle plot

app.layout = html.Div([
  html.H1(children="Hello World")
])

if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


