# for invoking files from different folders
import sys
sys.path.insert(0, r'C:\Users\liewg\Desktop\tebiki at created 27-06-2024\treeview-git\EnterpriseTreeView')

from CreateNodeAPI.get_treeview_data import getCompanyJson
from CreateNodeAPI.lambda_function import lambda_handler

# define test values 

# test get_treeview_data.py 
test_corporate_number = "3010001008848" # 日本製鉄株式会社 
# test lambda_function.py 
test_event= {
  "queryStringParameters": {
    "corporate_number": test_corporate_number
  }
}


if __name__ == "__main__":
    print("starts")

    # test get_treeview_data.py 
    treeview_data , copy_paste_data =getCompanyJson(test_corporate_number)
    print("==treeview_data=\n",treeview_data)
    print("==copy_paste_data=\n",copy_paste_data)
    
    # test lambda_function.py 
    http_response =lambda_handler(test_event,context="")
    print("==http_response=\n",http_response)    