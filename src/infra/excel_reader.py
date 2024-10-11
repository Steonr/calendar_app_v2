# import pandas lib as pd
import pandas as pd
import openpyxl
import xlrd

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

shiften = { "V34" : {
            "startUur" : "07:30",
            "eindUur" : "15:36",
            "kleur" : "blue"},

            "V38" : {
            "startUur" : "07:42",
            "eindUur" : "17:00",
            "kleur" : "bold green"},

            "D23" : {
            "startUur" : "08:00",
            "eindUur" : "16:06",
            "kleur" : "purple"},

            "D52" : {
            "startUur" : "08:30",
            "eindUur" : "17:00",
            "kleur" : "red"},

            "L32" : {
            "startUur" : "15:12",
            "eindUur" : "19:00",
            "kleur" : "yellow"},

            "L06" : {
            "startUur" : "12:42",
            "eindUur" : "20:48",
            "kleur" : "turquoise"},

            "D76" : {
            "startUur" : "10:00",
            "eindUur" : "13:12",
            "kleur" : "gray"},

            "ADV" : {
            "startUur" : "08:00",
            "eindUur" : "11:48",
            "kleur" : "bold blue"},

            "VRIJ" : {
            "startUur" : "00:00",
            "eindUur" : "23:59",
            "kleur" : "red"},

            "V" : {
            "startUur" : "08:00",
            "eindUur" : "11:48",
            "kleur" : "bold blue"}      
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
        self.df = DataFrame
    def remove_empty_values(self):
        self.data = self.df.drop([0,1,2])
        self.data = self.data.dropna()
    def string_to_dates(self):
        # Replace month names with their corresponding numbers
        self.data['Month'] = self.data['Month'].map(month_mapping)        
        # Convert Year, Month, and Day into a DateTime
        self.data['Date'] = pd.to_datetime(self.data[['Year', 'Month', 'Day']])
        self.data = self.data[['Year', 'Month', 'Day', 'Date', 'Shift']]
    def get_shiften_df(self):
        pass
    def set_column_names(self):
        self.df.dropna(inplace=True)
        self.df = self.df.set_axis(['Date', 'Week', 'Day', 'Shift'], axis=1)
        data = self.df['Date'].str.split(" ", n=1, expand=True)
        self.df["Year"] = data[1]
        self.df["Month"] = data[0]
        self.df.drop(columns=["Date"], inplace=True)
        self.df = self.df[['Year', 'Month', 'Week', 'Day', 'Shift']]

if __name__ == "__main__":
    path = './src/data/attachments/2de kwartaal 2024.xlsx'
    excel_reader = ExcelDataExtracter(path, "NUYTS CHRISTINE")
    df = excel_reader.get_df()
    process = ProcessDataFrame(df)
    process.set_column_names()
    process.remove_empty_values()
    process.string_to_dates()
    print(process.data)