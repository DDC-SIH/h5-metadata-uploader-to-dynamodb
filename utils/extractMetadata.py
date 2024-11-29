import h5py
import numpy as np

def get_h5_metadata(file_path):
    metadata = {}
    with h5py.File(file_path, 'r') as f:
        for key in f.attrs.keys():
            value = f.attrs[key]
            if isinstance(value, (list, tuple)):
                metadata[key] = value.tolist()
            elif isinstance(value, bytes):
                metadata[key] = value.decode('utf-8')
            elif isinstance(value, np.ndarray):
                metadata[key] = value.tolist()
            else:
                metadata[key] = value
    return metadata