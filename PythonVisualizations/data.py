import pandas as pd


def get_country_exports():
  """Gets the data from the csv file

  Returns:
      DataFrame: A DataFrame object with the data from the csv
  """
  country_exports_data = pd.read_csv('_data/exports.csv')
  return country_exports_data