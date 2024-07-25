"""
===================================
Description:
    The purpose of this class is to fill an empty cell of a pandas dataframe. 
    The dataframe reresents a company hiearchal data.
Author:
    Koki Yamanaka
Date:
    25-06-2024
===================================
"""

import pandas as pd
import os

class FillEmptyUnit:
    def __init__(self, df, col_pairs):
        """
        Initialize the class with a DataFrame and a list of column pairs.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        col_pairs (list of tuples): A list of tuples where each tuple contains
                                    (col_fill, col_reference).
        """
        self.df = df
        self.col_pairs = col_pairs
        self.replacementDictionary = {}

    def get_dictionary(self, col_reference):
        """Initialize an empty dictionary and fill it with unique values from the reference column."""
        unique_dict = {}
        for _, row in self.df.iterrows():
            key = row[col_reference]
            value = "missing_" + str(key)
            if key not in unique_dict:
                unique_dict[key] = value
        return unique_dict

    def fill_all_missing_with_unique_string(self):
        """Fill all missing values in the DataFrame with an empty string."""
        self.df = self.df.replace("", "N/A")


    def fill_empty_cells(self):
        """Fill the empty cells in the DataFrame based on the reference columns."""
        for col_fill, col_reference in self.col_pairs:
            replacement_dictionary = self.get_dictionary(col_reference)
            for index, row in self.df.iterrows():
                # only fill missing value if interest of fill column is empty and the reference column is not empty 
                # e.g. "headquarter" = missing and "division" = r&d lexus 
                if str(row[col_fill]) == "N/A" :
                    self.df.loc[index, col_fill] = replacement_dictionary[row[col_reference]]

    def get_updated_dataframe(self):
        """Return the updated DataFrame."""
        self.fill_all_missing_with_unique_string()
        self.fill_empty_cells()
        return self.df

    def get_dataframe(self): 
        return self.df
    
 
