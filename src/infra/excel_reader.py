from infra.ultility import invert_rows_cols

import numpy as np
import pandas as pd
import openpyxl
import xlrd

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

