
import pandas as pd

def load_data(file_path_or_buffer):
    if hasattr(file_path_or_buffer, 'read'):
        name = file_path_or_buffer.name
        if name.endswith('.csv'):
            return pd.read_csv(file_path_or_buffer)
        elif name.endswith('.xlsx'):
            return pd.read_excel(file_path_or_buffer)
        elif name.endswith('.json'):
            return pd.read_json(file_path_or_buffer)
        else:
            raise ValueError('Unsupported file type')
    else:
        if file_path_or_buffer.endswith('.csv'):
            return pd.read_csv(file_path_or_buffer)
        elif file_path_or_buffer.endswith('.xlsx'):
            return pd.read_excel(file_path_or_buffer)
        elif file_path_or_buffer.endswith('.json'):
            return pd.read_json(file_path_or_buffer)
        else:
            raise ValueError('Unsupported file type')
