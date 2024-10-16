import json

class ConfigLoader:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def get_data_paths(self):
        return self.config['data_paths']

    def get_request(self):
        return self.config['request']

    def get_message(self):
        return self.config['message']

    def get_shiften(self):
        return self.config['shiften']
    def get_excel(self):
        return self.config['excel']