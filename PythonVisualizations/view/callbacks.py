from dash.dependencies import Input, Output
from visualizations.icicle_plots import create_icicle_from_section, create_icicle_plot


def register_callbacks(app, exportations_data):
    @app.callback(
        Output("hs2-dropdown", "options"),
        Output("left-right-icicle", "figure"),
        Input("section-dropdown", "value")
    )
    def on_section_selected(selected_section):
        if selected_section:
            section_products = exportations_data[exportations_data["Section"] == selected_section]
            # Get hs2 groups by section name
            hs2_groups = section_products["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            # Create icicle plot
            section_icicle_plot = create_icicle_from_section(section_products)
            return hs2_dropdown_options, section_icicle_plot
        else:
            product_sections = list(exportations_data["Section"].unique())
            return [{"label": i, "value": i} for i in product_sections], create_icicle_plot(exportations_data)