import subprocess
import json
from utils.gdal_metadata import get_gdal_metadata
# from utils.extractMetadata import get_h5_metadata
# from utils.uploadToDynamoDB import upload_to_dynamodb
from utils.uploadToDynamoDbNew import upload_to_dynamodb

# Path to your HDF5 file
file_path = '3DIMG_12JUN2024_0830_L1C_ASIA_MER_V01R00.h5'

# Call the function to extract metadata using GDAL
metadata = get_gdal_metadata(file_path)

# Check if metadata was successfully retrieved
if metadata:
    # Convert metadata to JSON
    metadata_json = json.dumps(metadata, indent=4)
    print(metadata_json)

    # Save the metadata to a JSON file
    json_file_path = 'metadata.json'
    with open(json_file_path, 'w') as f:
        f.write(metadata_json)

    # Upload JSON data to DynamoDB (uncomment if needed)
    table_name = 'Files'
    upload_to_dynamodb(json_file_path, table_name)
else:
    print("Failed to extract metadata.")