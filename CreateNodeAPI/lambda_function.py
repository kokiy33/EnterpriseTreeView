import json
from createNode import getCompanyNode # function
def lambda_handler(event, context):
    # Extract query string parameters
    x = event['queryStringParameters']['x']
    y = event['queryStringParameters']['y']
    op = event['queryStringParameters']['op']
    
    # Log inputs
    print(f"x:{x}, y:{y}, op:{op}")
    
    # test (fake) corporate number 
    str cor_num = "4242"
    # Prepare the response body
    res_body = {
        'x': int(x),
        'y': int(y),
        'op': op,
        'ans': getCompanyNode(cor_num)
    }
    
    # Prepare HTTP response
    http_res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(res_body)
    }
    
    return http_res

