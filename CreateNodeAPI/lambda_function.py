import json
from getCompanyNode import getCompanyJson # function
def lambda_handler(event, context):
    # Extract query string parameters
    corporate_number = event['queryStringParameters']['corporate_number']

    # Log inputs
    print(f"corporate_number:{corporate_number}")
    
    # Prepare the response body
    res_body = {
        'corporate_number': int(corporate_number),
        'ans': getCompanyJson(corporate_number)
    }
    
    # Prepare HTTP response
    http_res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            # CORS policy
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "https://www.example.com",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(res_body)
    }
    
    return http_res

