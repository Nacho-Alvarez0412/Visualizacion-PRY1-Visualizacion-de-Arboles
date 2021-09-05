from dash.dependencies import Input, Output
from visualizations.icicle_plots import create_icicle_from_section, create_icicle_plot, create_icicle_from_hs2


def register_callbacks(app, exportations_data):
    @app.callback(
        Output("hs2-dropdown", "options"),
        Output("left-right-icicle", "figure"),
        Input("section-dropdown", "value"),
        Input("hs2-dropdown", "value")
    )
    def filter_horizontal_icicle_products(selected_section, selected_hs2):
        """Filters products by section and HS2

        :param selected_section: The section selected
        :param selected_hs2: The hs2 selected
        :return: The new hs2 dropdown and horizontal icicle
        """
        if (not selected_section and not selected_hs2) or (not selected_section and selected_hs2):
            return [], create_icicle_plot(exportations_data)
        elif selected_section and not selected_hs2:
            section_products = exportations_data[exportations_data["Section"] == selected_section]
            # Get hs2 groups by section name
            hs2_groups = section_products["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            section_icicle_plot = create_icicle_from_section(section_products)
            return hs2_dropdown_options, section_icicle_plot
        elif selected_section and selected_hs2:
            hs2_groups = exportations_data[exportations_data["Section"] == selected_section]["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            filtered_products = exportations_data[
                                    (exportations_data["Section"] == selected_section)
                                    & (exportations_data["HS2"] == selected_hs2)]
            # No products with section and hs2
            if filtered_products.empty:
                section_products = exportations_data[exportations_data["Section"] == selected_section]
                section_icicle_plot = create_icicle_from_section(section_products)
                return hs2_dropdown_options, section_icicle_plot

            hs2_icicle_plot = create_icicle_from_hs2(filtered_products)
            return hs2_dropdown_options, hs2_icicle_plot