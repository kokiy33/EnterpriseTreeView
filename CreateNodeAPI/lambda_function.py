import json
from getCompanyNode import getCompanyJson # function
import base64

def lambda_handler(event,context):
    # Extract query string parameters
    corporate_number = event['queryStringParameters']['corporate_number']

    # Log inputs
    print(f"corporate_number:{corporate_number}")

    # # returns a list of dict element
    treeview_data = getCompanyJson(corporate_number)

    # Prepare the response body2
    res_body = {
        'corporate_number': int(corporate_number),
        'display_data': treeview_data, # returns a list of dict containing parent-child relationship 
        # 'copy_paste_data' : copy_paste_data
    }
    
    # Prepare HTTP response
    http_res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8', # everything within response is utf-8 encoded 
            # CORS policy
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': res_body
    }

    return http_res

