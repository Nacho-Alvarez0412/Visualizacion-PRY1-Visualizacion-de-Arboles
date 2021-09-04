import dash
import pandas as pd
from dash.dependencies import Input, Output
from view.layout import create_main_layout


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

country_exports_data = pd.read_csv('_data/exports.csv')

app.layout = create_main_layout(country_exports_data)

@app.callback(
    Output("hs2-dropdown", "options"),
    Input("section-dropdown", "value")
)
def on_section_selected(selected_section):
    # Get hs2 groups by section name
    # TODO: Implement updates for icicle plot
    hs2_groups = country_exports_data[country_exports_data["Section"] == selected_section]["HS2"].unique()
    hs2_dropdown_options = [{"label": i, "value": i}  for i in list(hs2_groups)]
    return [{"label": i, "value": i}  for i in list(hs2_groups)]



if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


