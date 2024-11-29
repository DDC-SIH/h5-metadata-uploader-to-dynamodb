from utils.extractMetadata import get_h5_metadata
from utils.uploadToDynamoDB import upload_to_dynamodb
import json

# Path to your HDF5 file
file_path = '3DIMG_12JUN2024_0830_L1C_ASIA_MER_V01R00.h5'
metadata = get_h5_metadata(file_path)

# Convert metadata to JSON
metadata_json = json.dumps(metadata, indent=4)
print(metadata_json)

# Make the JSON file in the same directory
json_file_path = 'metadata.json'
with open(json_file_path, 'w') as f:
    f.write(metadata_json)

# Upload JSON data to DynamoDB
table_name = 'Files'
upload_to_dynamodb(json_file_path, table_name)