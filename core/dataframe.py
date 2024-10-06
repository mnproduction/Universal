# core/dataframe.py

import pandas as pd

class DataFrameProcessor:
    def __init__(self, data: dict):
        self.data = data

    def create_dataframe(self) -> pd.DataFrame:
        if isinstance(self.data, dict):
            # If the data is a dictionary containing lists, assume these lists are records
            data_for_df = next(iter(self.data.values())) if len(self.data) == 1 else self.data
        elif isinstance(self.data, list):
            data_for_df = self.data
        else:
            raise ValueError("Data is neither a dictionary nor a list, cannot convert to DataFrame")

        df = pd.DataFrame(data_for_df)
        return df

