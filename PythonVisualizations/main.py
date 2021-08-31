import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
import data


# Read exports data
country_exports = data.get_country_exports()
# Create icicle plot
fig = px.icicle(country_exports, path=[px.Constant('Exportaciones en Costa Rica'), 'Section', 'HS2', 'HS4'], values='Trade Value')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

app = dash.Dash()
app.layout = html.Div([
  html.H1(children="Hello World"),
  dcc.Graph(figure=fig),
])

app.run_server(debug=True, port=4000, use_reloader=True)
