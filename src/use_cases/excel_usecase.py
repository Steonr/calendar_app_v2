from infra.config_loader import ConfigLoader
from infra.ultility import get_file_names
from infra.excel_reader import ExcelDataExtracter
from infra.data_processing import ProcessShiftenData

import numpy as np

class ExcelUseCase:
    def __init__(self):
        self._config_loader = ConfigLoader('./config.json')
        self._data_paths = self._config_loader.get_data_paths()
        self._excel = self._config_loader.get_excel()
        self._excel_dir = self._data_paths['attachment']
        self._name = self._excel['name']
        self._out_path = self._data_paths['out_path']
    def read_excel(self):
        file_names = get_file_names(self._excel_dir)
        file_paths = []

        for file_name in file_names:
            file_type = file_name.split('.')[1]
            if file_type == ('xls' or 'xlsx'):           
                file_paths.append(str(self._excel_dir+file_name)) 

        excel_reader = ExcelDataExtracter(file_paths[0], self._name)
        file_paths.pop(0)

        df = excel_reader.get_df()
        process = ProcessShiftenData(df)
        process.clean_up_data()

        for path in file_paths:
            excel_reader = ExcelDataExtracter(path, self._name)
            df = excel_reader.get_df()
            _process = ProcessShiftenData(df)
            _process.clean_up_data()
            process.add_data(_process.get_data())

        process.data['start_time'].replace('', np.nan, inplace=True)
        process.data = process.data.dropna()
        process.data.to_excel(f'{self._out_path}all_data.xlsx', engine='xlsxwriter')  
        print(process.data)