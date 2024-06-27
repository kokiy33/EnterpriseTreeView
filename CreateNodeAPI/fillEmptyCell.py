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

    def set_dictionary(self, col_fill, col_reference):
        """Initialize an empty dictionary and fill it with unique values from the reference column."""
        unique_dict = {}
        for _, row in self.df.iterrows():
            key = row[col_reference]
            value = "missing_" + str(key)
            if key not in unique_dict:
                unique_dict[key] = value
        unique_dict[""] = "missing_" + col_fill  # add empty string case
        self.replacementDictionary[(col_fill, col_reference)] = unique_dict

    
    def fill_empty_cells(self):
        """Fill the empty cells in the DataFrame based on the reference columns."""
        for col_fill, col_reference in self.col_pairs:
            self.set_dictionary(col_fill, col_reference)
            for index, row in self.df.iterrows():
                if pd.isna(row[col_fill]):
                    self.df.loc[index, col_fill] = self.replacementDictionary[(col_fill, col_reference)][row[col_reference]]

    def get_dataframe(self):
        """Return the updated DataFrame."""
        self.fill_empty_cells()
        return self.df
