import boto3
import json
from decimal import Decimal

# Custom JSONEncoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)  # Convert Decimal to float
        return super().default(o)

def remove_empty_keys(data):
    """
    Recursively removes empty keys from a JSON-like dictionary.
    """
    if isinstance(data, dict):
        return {
            key if key else "UNKNOWN_KEY": remove_empty_keys(value)
            for key, value in data.items()
            if key is not None and key.strip() != ""
        }
    elif isinstance(data, list):
        return [remove_empty_keys(item) for item in data]
    else:
        return data

def process_json(data):
    """
    Processes JSON data to flatten single-value lists into scalar values
    and handles empty string keys in dictionaries.
    """
    for key, value in list(data.items()):
        # Handle empty string keys
        if key == "":
            data["default"] = data.pop(key)  # Replace empty key with "default"

        # Recursively process nested dictionaries
        if isinstance(value, dict):
            data[key] = process_json(value)

        # Flatten single-value lists into scalar
        elif isinstance(value, list) and len(value) == 1:
            data[key] = value[0]
        elif isinstance(value, list):
            data[key] = [Decimal(str(v)) if isinstance(v, float) else v for v in value]
        elif isinstance(value, float):
            data[key] = Decimal(str(value))  # Convert floats to Decimal

    # Add uniqueId field if it exists
    try:
        unique_id = data['metadata']['default']['Unique_Id']
        data['Unique_Id'] = unique_id
    except KeyError:
        print("uniqueId not found in processedMetaData.metadata.default")

    return remove_empty_keys(data)

def validate_data(data):
    """
    Validates that the data does not contain empty keys or invalid attributes.
    """
    for key in data.keys():
        if key == '' or key is None:  # If key is empty string or None
            raise ValueError(f"Found empty or None attribute name: '{key}'")
    return True

def upload_to_dynamodb(json_file_path, table_name, region_name='ap-south-1'):
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session(
        region_name=region_name,
        aws_access_key_id='add key here',
        aws_secret_access_key='add key here'
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f, parse_float=Decimal)  # Convert floats to Decimals

    # Process the JSON data
    processed_data = process_json(data)

    # Validate data before uploading
    try:
        validate_data(processed_data)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Log the processed data for debugging (converted to JSON string)
    print("Processed Data: ", json.dumps(processed_data, cls=DecimalEncoder, indent=2))

    # Upload the item to DynamoDB
    try:
        table.put_item(Item=processed_data)
        print(f"Processed data from {json_file_path} has been uploaded to {table_name} table.")
    except Exception as e:
        print(f"Error uploading to DynamoDB: {e}")
