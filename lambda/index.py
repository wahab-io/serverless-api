def handler(event, context):
    """
    Lambda function handler that serves as a proxy for API Gateway.
    
    Parameters:
    event (dict): API Gateway event
    context (object): Lambda context
    
    Returns:
    dict: API Gateway response
    """
    print('Request:', event)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message": "Hello from Lambda!", "version": "1.0.0"}'
    }
