'''CSV modules'''
import pandas as pd
from typing import List, Dict
'''
Usage:
    csv_bytes = file.file.read() # file: UploadFile = File(...)
    buffer = BytesIO(csv_bytes)

'''


class PandasCsv:
    '''Pandas Helpers'''

    @staticmethod
    def read_csv_urls(file_name, column_index=''):
        """Read the CSV file and extract a specific column."""
        df = pd.read_csv(file_name)
        # Extract the specified column
        urls = df[column_index].drop_duplicates().to_list()
        return urls
    
    @staticmethod
    def read_csv_to_list(file_name):
        """Read the CSV file and return as list"""
        df = pd.read_csv(file_name)
        # convert to list of dictionary
        data_list: List[Dict[str, any]] = df.drop_duplicates().to_dict(orient='records')
        return data_list
    
    @staticmethod
    def write_data_to_csv(data, file_name):
        """Write data to a CSV file using pandas."""
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
        return
