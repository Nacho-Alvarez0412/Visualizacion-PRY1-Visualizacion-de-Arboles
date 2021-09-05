from dash.dependencies import Input, Output


def register_callbacks(app, exportations_data):
    @app.callback(
        Output("hs2-dropdown", "options"),
        Input("section-dropdown", "value")
    )
    def on_section_selected(selected_section):
        # Get hs2 groups by section name
        # TODO: Implement updates for icicle plot
        hs2_groups = exportations_data[exportations_data["Section"] == selected_section]["HS2"].unique()
        hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
        return [{"label": i, "value": i} for i in list(hs2_groups)]