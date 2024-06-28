"""
===================================
Description:
    The purpose of this program is to receive coporate  
Author:
    Koki Yamanaka
Date:
    25-06-2024
===================================
"""
import pandas as pd 
import os 

def get_unfilled_company_df(companyName):
    # Use os.path.join for cross-platform compatibility
    filepath = os.path.join( companyName + ".csv")
    
    # Print the file path for debugging purposes
    print("File path:", filepath)
    
    # Check if the file exists before trying to read it
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    return pd.read_csv(filepath)
 