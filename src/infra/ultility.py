from infra.config_loader import ConfigLoader

import json
from os import walk


def get_json(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_file_names(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return filenames

def dim(a):
    return [] if type(a) != list else [len(a)] + dim(a[0])

def invert_rows_cols(data_list):
    dimension = dim(data_list)
    return [
            [data_list[0][i], data_list[1][i], data_list[2][i], data_list[3][i]]
            for i in range(dimension[-1])
    ]
            
    
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