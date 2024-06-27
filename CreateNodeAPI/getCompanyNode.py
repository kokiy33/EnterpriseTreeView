"""
===================================
Description: 
    (Main) program to receive hierarchal data of a company. 

    The program purpose is to return the hierarchal data structure of a specified company (specified by FORCAS corporate number) in JSON format.  
    Is is done by invoking a chain of programs getCompanyCsv.py, fillEmptyCell.py, createNode.py.  
Author:
    Koki Yamanaka
Date:
    25-06-2024
===================================
"""

from getCompanyCsv import get_unfilled_company_df # get_unfilled_company_df is a function 
from fillEmptyCell import FillEmptyUnit # file + class 
from createNode import DataframeToNodeConverter

def createCompanyNameCol(df,companyName:str):
    df["companyName"] = companyName
    return df 

def getCompanyNode(corporate_number :str): 
    companyName = "mitsui.csv"
    
    # Specify columns to fill the empty cells 
    col_pairs = [("headquarter", "division"), ("division", "department"), ("department", "section")]  
    
    # Get data from papatto, convert to CSV 
    unfilled_corporate_df = get_unfilled_company_df() 
    print("Unfilled corporate DataFrame:")
    
    # Fill the empty cells with empty "missing" notation by using subsequent columns as a reference 
    fillEmptyUnitObj = FillEmptyUnit(df=unfilled_corporate_df, col_pairs=col_pairs)
    filled_corporate_df = fillEmptyUnitObj.get_dataframe()
    print("Filled corporate DataFrame:")

    # Create root companyname column
    filled_corporate_df = createCompanyNameCol(filled_corporate_df, companyName=companyName)
    print("Corporate DataFrame with company name column:")
    # print(filled_corporate_df)

    # Convert DataFrame to JSON node format
    NodeConvertObj = DataframeToNodeConverter(df=filled_corporate_df)
    json_data = NodeConvertObj.convert() # returns json in string 
    print("JSON output in string")

    return json_data