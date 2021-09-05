from dash.dependencies import Input, Output
from visualizations.charts import create_icicle_chart


def register_callbacks(app, exportations_data):
    def filter_sunburst_products(selected_section, selected_hs2):
        pass


    @app.callback(
        Output("horizontal-icicle-hs2-dropdown", "options"),
        Output("left-right-icicle", "figure"),
        Input("horizontal-icicle-section-dropdown", "value"),
        Input("horizontal-icicle-hs2-dropdown", "value")
    )
    def filter_horizontal_icicle_products(selected_section, selected_hs2):
        """Filters products by section and HS2

        :param selected_section: The section selected
        :param selected_hs2: The hs2 selected
        :return: The new hs2 dropdown and horizontal icicle
        """
        if (not selected_section and not selected_hs2) or (not selected_section and selected_hs2):
            return [], create_icicle_chart(exportations_data)
        elif selected_section and not selected_hs2:
            section_products = exportations_data[exportations_data["Section"] == selected_section]
            # Get hs2 groups by section name
            hs2_groups = section_products["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            section_icicle_plot = create_icicle_chart(section_products, chart_type="section")
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
                section_icicle_plot = create_icicle_chart(section_products, chart_type="section")
                return hs2_dropdown_options, section_icicle_plot

            hs2_icicle_plot = create_icicle_chart(filtered_products, chart_type="hs2")
            return hs2_dropdown_options, hs2_icicle_plot


    @app.callback(
        Output("vertical-icicle-hs2-dropdown", "options"),
        Output("vertical-icicle", "figure"),
        Input("vertical-icicle-section-dropdown", "value"),
        Input("vertical-icicle-hs2-dropdown", "value")
    )
    def filter_vertical_icicle_products(selected_section, selected_hs2):
        """Filters the products of the vertical icicle plot

        :param selected_section: The selection used to filter the products
        :param selected_hs2: The HS2 used to filter the products
        :return: The updated HS2 dropdown and vertical icicle plot
        """
        if (not selected_section and not selected_hs2) or (not selected_section and selected_hs2):
            return [], create_icicle_chart(exportations_data, orientation="v")
        elif selected_section and not selected_hs2:
            section_products = exportations_data[exportations_data["Section"] == selected_section]
            # Get hs2 groups by section name
            hs2_groups = section_products["HS2"].unique()
            hs2_dropdown_options = [{"label": i, "value": i} for i in list(hs2_groups)]
            section_icicle_plot = create_icicle_chart(section_products, chart_type="section", orientation="v")
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
                section_icicle_plot = create_icicle_chart(section_products, chart_type="section", orientation="v")
                return hs2_dropdown_options, section_icicle_plot

            hs2_icicle_plot = create_icicle_chart(filtered_products, chart_type="hs2", orientation="v")
            return hs2_dropdown_options, hs2_icicle_plot