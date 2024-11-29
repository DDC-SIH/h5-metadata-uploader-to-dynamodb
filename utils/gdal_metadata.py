import subprocess
import json

def get_gdal_metadata(h5_file_path):
    """
    Function to get metadata from an HDF5 file using gdalinfo and return it as a JSON object.
    
    Args:
    h5_file_path (str): The path to the HDF5 file.
    
    Returns:
    dict: Metadata of the HDF5 file as a JSON object.
    """
    try:
        # Run the gdalinfo command and capture the output
        result = subprocess.run(['gdalinfo', h5_file_path, '-json'], capture_output=True, text=True, check=True)
        
        # Parse the output to JSON
        metadata = json.loads(result.stdout)
        
        return metadata
    
    except subprocess.CalledProcessError as e:
        print(f"Error while running gdalinfo: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
