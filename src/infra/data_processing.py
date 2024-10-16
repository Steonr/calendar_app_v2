import pandas as pd
import numpy as np

from infra.ultility import month_mapping
from infra.config_loader import ConfigLoader

class ProcessShiftenData:
    def __init__(self, DataFrame):
        self._df = DataFrame
        self.data = np.nan
    def set_data(self, data):
        if type(data) == type(pd.DataFrame()):
            self.data = data
        else:
            print(f'Data is {type(data)} and not of type {type(pd.DataFrame())}')
    def add_data(self, data):
        if type(data) != type(pd.DataFrame()):
            print(f'Data is {type(data)} and not of type {type(pd.DataFrame())}')
            return
        data = pd.concat([self.get_data(), data], ignore_index=True)
        self.set_data(data)
    def get_data(self):
        return self.data
    def clean_up_data(self):
        self._set_column_names()
        self._remove_empty_values()
        self._string_to_dates()
        self._add_dictionary_data()
    def _remove_empty_values(self):
        self.data = self._df.drop([0,1,2])
        self.data = self.data.dropna()
    def _string_to_dates(self):
        # Replace month names with their corresponding numbers
        self.data['Month'] = self.data['Month'].map(month_mapping)        
        # Convert Year, Month, and Day into a DateTime
        self.data['Date'] = pd.to_datetime(self.data[['Year', 'Month', 'Day']])
        self.data = self.data[['Year', 'Month', 'Day', 'Date', 'Shift']]
    def get_shiften_df(self):
        pass
    def _set_column_names(self):
        self._df.dropna(inplace=True)
        self._df = self._df.set_axis(['Date', 'Week', 'Day', 'Shift'], axis=1)
        data = self._df['Date'].str.split(" ", n=1, expand=True)
        self._df["Year"] = data[1]
        self._df["Month"] = data[0]
        self._df.drop(columns=["Date"], inplace=True)
        self._df = self._df[['Year', 'Month', 'Week', 'Day', 'Shift']]
    def _add_dictionary_data(self):
        config_loader = ConfigLoader("./config.json")
        shiften = config_loader.get_shiften()
        # Create new columns for start_time, end_time, and color using map
        self.data['start_time'] =  self.data['Shift'].map(lambda x: shiften[x]["start_time"] if x in shiften else "")
        self.data['end_time'] =  self.data['Shift'].map(lambda x: shiften[x]["end_time"] if x in shiften else "")
        self.data['color'] =  self.data['Shift'].map(lambda x: shiften[x]["color"] if x in shiften else "")