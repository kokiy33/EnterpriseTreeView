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

def get_unfilled_company_df():
    return pd.read_csv(r"EnterpriseTreeView\nodeCreateAPI\三井化学株式会社.csv")
