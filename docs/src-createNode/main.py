import createNode
import modifyNode 
import json
import os
import pandas as pd 

def exportNode(output_file_path, processed_nodes): 
    """Saves the processed nodes to a JSON file."""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_nodes, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    
    # input - needs to add 'corporate_number.csv' at the end 
    base_pregraph_path  = r"C:\Users\liewg\Desktop\Tebiki files\organization_chart_project\treeview\data\pregraph"
    # output - needs to add 'corporate_number.json' at the end 
    base_postgraph_path = r"C:\Users\liewg\Desktop\Tebiki files\organization_chart_project\treeview\data\postgraph"

    # Get the list of files in the pregraph directory
    files = os.listdir(base_pregraph_path)

    # Loop through each file and concatenate with the base path
    for filename in files:
        full_path = os.path.join(base_pregraph_path, filename) 
        
        # read csv as df 
        read_df = pd.read_csv(full_path)

        # modify node 
        modified_df = modifyNode.fill_missing_parents(read_df)

        # connect root node 
        company_name  = filename.replace('.csv', '')
        modified_df = modifyNode.connect_root_node(df=modified_df,company_name= company_name)

        # dataframe to node structure in json 
        node_object = createNode.DataframeToNodeConverter(df=modified_df)
        convertedNode = node_object.convert()  # Returns a list of nodes. 

        output_file_path = os.path.join(base_postgraph_path, filename.replace(".csv", ".json"))
        exportNode(output_file_path, convertedNode)
