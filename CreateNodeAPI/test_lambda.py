import json
from lambda_function import lambda_handler

event = {
    "queryStringParameters": {
        "corporate_number": "3010001008848"
    }
}
context = {}

response = lambda_handler(event, context)
print(json.dumps(response, indent=4))

# Write the response to a JSON file
outputpath = r"C:\Users\liewg\Desktop\tebiki at created 27-06-2024\treeview-git\EnterpriseTreeView\CreateNodeAPI\response.json"
with open(outputpath, 'w') as json_file:
    json.dump(response, json_file, indent=4)