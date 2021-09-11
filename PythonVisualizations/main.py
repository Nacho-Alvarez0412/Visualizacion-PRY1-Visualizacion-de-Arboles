import dash
import pandas as pd
from view.layout import create_main_layout
from view.callbacks import register_callbacks


external_stylesheets = ['./assets/css/style.css']
app = dash.Dash(title="Costa Rica Exports", external_stylesheets=external_stylesheets)

country_exports_data = pd.read_csv('_data/test.csv')

app.layout = create_main_layout(country_exports_data)
register_callbacks(app, country_exports_data)

if __name__ == "__main__":
  app.run_server(debug=True, port=4000, use_reloader=True)


