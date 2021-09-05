from dash.dependencies import Input, Output
from visualizations.icicle_plots import create_icicle_from_section, create_icicle_plot


def register_callbacks(app, exportations_data):
    @app.callback(
        Output("hs2-dropdown", "options"),
        Output("left-right-icicle", "figure"),
        Input("section-dropdown", "value"),
        Input("hs2-dropdown", "value")
    )
    def on_section_selected(selected_section, selected_hs2):
        """Updates the icicle plot and the HS2 dropdown

        :param selected_section: The section used to filter the data
        :return: The new dropdown and icicle using the selected section
        """
        if not selected_section and not selected_hs2:
            return [], create_icicle_plot(exportations_data)
        elif selected_section and not selected_hs2:
            section_products = exportations_data[exportations_data["Section"] == selected_section]
            # Get hs2 groups by section name
            hs2_groups = section_products["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            # Create icicle plot
            section_icicle_plot = create_icicle_from_section(section_products)
            return hs2_dropdown_options, section_icicle_plot
        elif selected_section and selected_hs2:
            # Get products by section and by hs2
            filtered_products = exportations_data[
                                    (exportations_data["Section"] == selected_section)
                                    & (exportations_data["HS2"] == selected_hs2)
                               ]
            # Get hs2 groups by section name
            hs2_groups = exportations_data[exportations_data["Section"] == selected_section]["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            # Create icicle plot
            # section_icicle_plot = create_icicle_from_section(section_products)
            # TODO: Create icicle plot for both filters
            return hs2_dropdown_options, None