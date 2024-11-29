import json
from utils.gdal_metadata import get_gdal_metadata
from utils.uploadToDynamoDbNew import upload_to_dynamodb

# Path to your HDF5 file
file_path = '3DIMG_12JUN2024_0830_L1C_ASIA_MER_V01R00.h5'

# Call the function to extract metadata using GDAL
metadata = get_gdal_metadata(file_path)

# Check if metadata was successfully retrieved
if metadata:
    # Print the extracted metadata
    print("Extracted Metadata:")
    print(json.dumps(metadata, indent=4))

    # Upload metadata directly to DynamoDB
    table_name = 'Files'
    upload_to_dynamodb(metadata, table_name)
else:
    print("Failed to extract metadata.")
