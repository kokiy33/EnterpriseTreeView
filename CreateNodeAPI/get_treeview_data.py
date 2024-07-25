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
from org_info.generator import OrgInfoGenerator
from fill_empty_cells import FillEmptyUnit # file + class 
from convert_child_parents import DataframeToNodeConverter

import json 
import pandas as pd 

import time 


def createCompanyNameCol(df,companyName:str):
    df["companyName"] = companyName
    return df 

 
def getCompanyJson(corporate_number: str): 
    start_time = time.time()  # Capture the start time
    
    # Specify columns to fill the empty cells 
    col_pairs = [("headquarter", "division"), ("division", "department"), ("department", "section")]  
    
    # Get data from papatto, convert to dataframe object 
    org_infos = OrgInfoGenerator.generate(corporate_number)  # get response 
    return org_infos
org_infos = getCompanyJson("4010401052081")
print(org_infos)
print(type(org_infos))
print(type(org_infos[0]))

    # org_infos_df = pd.DataFrame(org_infos)
    # org_infos_df.to_csv('raw.csv')
    # print("0. Complete retrieving raw data from papatto\n")

    # # # Fill the empty cells with empty "missing" notation by using subsequent columns as a reference 
    # fillEmptyUnitObj = FillEmptyUnit(df=org_infos_df, col_pairs=col_pairs)
    # filled_corporate_df = fillEmptyUnitObj.get_updated_dataframe()
    # print("1. Completed filling corporate DataFrame\n")
    # filled_corporate_df.to_csv('filled.csv')

    # # # Create root companyname column
    # filled_corporate_df = createCompanyNameCol(filled_corporate_df, companyName=corporate_number)
    # print("2. Completed binding company name (root)\n")
    # filled_corporate_df.to_csv('root.csv')
    
    # # # Convert DataFrame to JSON node format
    # NodeConvertObj = DataframeToNodeConverter(df=filled_corporate_df)
    # treeview_data = NodeConvertObj.convert()  # returns a list of dict object
    # print("3. Completed convert dataframe to treeview structure")
    # # Save data to a JSON file

    # # For Copy and paste google sheet 
    # copy_paste_data = org_infos_df.to_dict(orient='records')

    # end_time = time.time()  # Capture the end time
    # execution_time = end_time - start_time  # Calculate the duration
    # print(f"Execution time: {execution_time:.2f} seconds")
    
    # return treeview_data ,  copy_paste_data  # returns an array of dict. 1. for treeview 2. for google sheet copy/paste

