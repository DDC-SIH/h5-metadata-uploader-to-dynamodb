import boto3
import json
from decimal import Decimal

def process_json(data):
    """
    Processes JSON data to flatten single-value lists into scalar values.
    """
    for key, value in data.items():
        if isinstance(value, list) and len(value) == 1:
            data[key] = value[0]  # Flatten single-value list into scalar
        elif isinstance(value, list):
            data[key] = [Decimal(str(v)) if isinstance(v, float) else v for v in value]
        elif isinstance(value, float):
            data[key] = Decimal(str(value))  # Convert floats to Decimal
    return data

def upload_to_dynamodb(json_file_path, table_name, region_name='ap-south-1'):
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session(
        region_name=region_name,
        aws_access_key_id='add here',
        aws_secret_access_key='add here dude'
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f, parse_float=Decimal)  # Convert floats to Decimals

    # Process the JSON data
    processed_data = process_json(data)

    # Upload the item to DynamoDB
    table.put_item(Item=processed_data)

    print(f"Processed data from {json_file_path} has been uploaded to {table_name} table.")


