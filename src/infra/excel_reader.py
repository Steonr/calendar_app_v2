from os import walk
import numpy as np
# import pandas lib as pd
import pandas as pd
import openpyxl
import xlrd

def get_file_names(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return filenames

month_mapping = {  
            "januari": 1,
            "februari": 2,
            "maart": 3,
            "april": 4,
            "mei": 5,
            "juni": 6,
            "juli": 7,
            "augustus": 8,
            "september": 9,
            "oktober": 10,
            "november": 11,
            "december": 12
        }

shiften = { "v34" : {
            "start_time" : "07:30",
            "end_time" : "15:36",
            "color" : "blue"},

            "v38" : {
            "start_time" : "07:42",
            "end_time" : "17:00",
            "color" : "bold green"},

            "d23" : {
            "start_time" : "08:00",
            "end_time" : "16:06",
            "color" : "purple"},

            "d52" : {
            "start_time" : "08:30",
            "end_time" : "17:00",
            "color" : "red"},

            "l32" : {
            "start_time" : "15:12",
            "end_time" : "19:00",
            "color" : "yellow"},

            "l06" : {
            "start_time" : "12:42",
            "end_time" : "20:48",
            "color" : "turquoise"},

            "d76" : {
            "start_time" : "10:00",
            "end_time" : "13:12",
            "color" : "gray"},

            "adv" : {
            "start_time" : "08:00",
            "end_time" : "11:48",
            "color" : "bold blue"},

            "vrij" : {
            "start_time" : "00:00",
            "end_time" : "23:59",
            "color" : "red"},

            "v" : {
            "start_time" : "08:00",
            "end_time" : "11:48",
            "color" : "bold blue"}      
            }

            
class ExcelReader:
    def __init__(self, path):
        self._pd = pd
        self._data = None
        self._path = path
    def get_data(self):
        return self._data

    def open_file(self):
        self._data = xlrd.open_workbook(self._path) 
    def _get_row_(self, row, index_num):
        sheet = self._data.sheet_by_index(index_num)
        return [sheet.cell_value(row,i).lower() for i in range(sheet.ncols)]
    def _get_column_(self, column_num, index_num):
        sheet = self._data.sheet_by_index(index_num)
        return [sheet.cell_value(i,column_num).lower() for i in range(sheet.nrows)]                



class ExcelDataExtracter(ExcelReader):
    def __init__(self, path, name):
        super().__init__(path)
        self.open_file()
        self.header = self._get_header()
        self.data_row = self._get_row(name)
    def _get_header(self):
        return [self._get_row_(i,0) for i in range(3)]

    def _get_row(self, name: str):
        name = name.lower()
        index = self._get_column_(0,0).index(name)
        return self._get_row_(index, 0)
    def get_df(self):
        data = self.header
        data.append(self.data_row)
        data_inv = invert_rows_cols(data)
        return self._pd.DataFrame(data_inv)


def dim(a):
    return [] if type(a) != list else [len(a)] + dim(a[0])

def invert_rows_cols(data_list):
    dimension = dim(data_list)
    return [
            [data_list[0][i], data_list[1][i], data_list[2][i], data_list[3][i]]
            for i in range(dimension[-1])
    ]
            

class ProcessDataFrame:
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
        # Create new columns for start_time, end_time, and color using map
        self.data['start_time'] =  self.data['Shift'].map(lambda x: shiften[x]["start_time"] if x in shiften else "")
        self.data['end_time'] =  self.data['Shift'].map(lambda x: shiften[x]["end_time"] if x in shiften else "")
        self.data['color'] =  self.data['Shift'].map(lambda x: shiften[x]["color"] if x in shiften else "")



if __name__ == "__main__":

    directory = './src/data/attachments/'
    out_path = './src/data/output/'
    file_names = get_file_names(directory)
    file_paths = [str(directory+file_name) for file_name in file_names]
    
    excel_reader = ExcelDataExtracter(file_paths[0], "NUYTS CHRISTINE")
    file_paths.pop(0)
    
    df = excel_reader.get_df()
    process = ProcessDataFrame(df)
    process.clean_up_data()
    
    for path in file_paths:
        excel_reader = ExcelDataExtracter(path, "NUYTS CHRISTINE")
        df = excel_reader.get_df()
        _process = ProcessDataFrame(df)
        _process.clean_up_data()
        process.add_data(_process.get_data())

    process.data['start_time'].replace('', np.nan, inplace=True)
    process.data = process.data.dropna()
    process.data.to_excel(f'{out_path}output1.xlsx', engine='xlsxwriter')  
    print(process.data)