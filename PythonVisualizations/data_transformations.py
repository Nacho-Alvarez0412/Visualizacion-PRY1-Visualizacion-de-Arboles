def create_hierarchical_structure(exports_dataframe, root_name="Exportaciones de Costa Rica"):
    """Creates a hierarchical data structure that can be used for generating icicle plots

    :param exports_dataframe: The dataframe with the exports data
    :param root_name: The name of the root element for the structure
    :return: A dictionary with the hierarchical structure
    """

    result = {"parents": [""], "elements": [root_name], "values": []}
    hs2_trade_values = []
    total_trades = 0

    for index, product in exports_dataframe.iterrows():
        if index == 0:
            result["elements"].append(product['Section'])
            result["parents"].append(root_name)
        # Check if section exists
        if not product["Section"] in result["elements"]:
            result["elements"].append(product['Section'])
            result["parents"].append(root_name)

            total_section_trades = add_section_values(result["values"], hs2_trade_values)
            total_trades += total_section_trades
            hs2_trade_values = []
        # Check if HS2 of section exists
        if not product["HS2"] in result["elements"]:
            result["elements"].append(product["HS2"])
            result["parents"].append(product["Section"])
            hs2_trade_values.append([])
        # Add new leaf to the tree
        result["elements"].append(product["HS4"])
        result["parents"].append(product["HS2"])
        hs2_trade_values[len(hs2_trade_values) - 1].append(product["Trade Value"])

    # Add trade values from last section
    total_trades += add_section_values(result["values"], hs2_trade_values)
    result["values"].insert(0, total_trades)

    return result


def create_section_hierarchical_structure(exportations_dataframe):
    """Creates a hierarchical structure using a section as the root of structure

    :param exportations_dataframe: The DataFrame that will be transformed
    :return: A dictionary with the hierarchical structure
    """
    result = {"parents": [""], "elements": [exportations_dataframe.iloc[0]["Section"]], "values": []}
    hs2_trade_values = []

    for index, product in exportations_dataframe.iterrows():
        # Check if HS2 of section has been inserted
        if not product["HS2"] in result["elements"]:
            result["parents"].append(product["Section"])
            result["elements"].append(product["HS2"])
            hs2_trade_values.append([])
        result["elements"].append(product["HS4"])
        result["parents"].append(product["HS2"])
        hs2_trade_values[len(hs2_trade_values) - 1].append(product["Trade Value"])

    add_section_values(result["values"], hs2_trade_values)
    return result


def add_section_values(values_list, section_values):
    """Calculates the trade value of the section and each of its hs2 groups

    :param values_list: The list that contains all of the trade values from all sections
    :param section_values: A matrix that has the trade values of each hs2 group and its products
    :return: The trade value of the whole section
    """
    new_values = []
    total_section_trades = 0

    for hs2_group in section_values:
        new_values.append(sum(hs2_group))
        total_section_trades += sum(hs2_group)
        for trade_value in hs2_group:
            new_values.append(trade_value)

    values_list.append(total_section_trades)
    values_list.extend(new_values)

    return total_section_trades