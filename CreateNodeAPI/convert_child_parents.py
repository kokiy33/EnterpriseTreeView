"""
===================================
Description:
    The purpose of this class is to receives a dataframe representing hiearchal data of a company, 
    then it converts to the data structure required for displaying tree view. 
    The output is in JSON.
Author:
    Koki Yamanaka
Date:
    25-06-2024
===================================
"""

"""
Responsibility : converting CSV data into a node-based data structure.
"""
import json

class DataframeToNodeConverter:
    def __init__(self, df):
        self.__df = df
        self.__nodes = []
        self.__unique_nodes = {}
        self.__unique_key = 1

    def convert(self):
        """returns a list of dictionaries represent child and parent relationships"""
        self.__create_search_key()
        self.__create_nodes()
        return self.__nodes

    def __create_search_key(self):
        source_column = ["companyName","headquarter", "division", "department", "section", "site"]
        self.__df['検索キー'] = (
            self.__df[source_column[0]].astype(str) + ';' + 
            self.__df[source_column[1]].astype(str) + ';' +
            self.__df[source_column[2]].astype(str) + ';' +
            self.__df[source_column[3]].astype(str) + ';' +
            self.__df[source_column[4]].astype(str) + ';' + 
            self.__df[source_column[5]].astype(str) + ';' 
        )

    def __create_nodes(self):
        # iterate each rows of csv 
        for index, row in self.__df.iterrows():
            self.__process_row(row)

    def __process_row(self, row):
        units = row['検索キー'].split(';')
        parent_key = None

        for unit in units:
            if unit != "nan": 
                node_key = self.__get_or_create_node(name=unit, parent_key=parent_key)
                parent_key = node_key

    def __get_or_create_node(self, name, parent_key):
        if name not in self.__unique_nodes:
            self.__unique_nodes[name] = self.__unique_key
            node = {
                "key": self.__unique_key,
                "name": name}
            if parent_key:
                node["parent"] = parent_key
            self.__nodes.append(node)
            self.__unique_key += 1
        return self.__unique_nodes[name]
    
    def get_df(self):
        return self.__df
    