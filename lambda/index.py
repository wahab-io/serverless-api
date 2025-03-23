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

    # Get function version from context
    function_version = context.function_version

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': f'{{"message": "Hello from new Lambda!", "version": "{function_version}"}}'
    }
