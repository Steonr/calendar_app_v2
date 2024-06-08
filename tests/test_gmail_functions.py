import sys
import os
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
main_dir_path = os.path.dirname(dir_name)

# print("copy", main_dir_path)

import unittest
from unittest.mock import patch, MagicMock
from src.lib.gmail_functions import get_creds, check_creds

class TestGmailFunctions(unittest.TestCase):

    @patch('src.lib.gmail_functions.os.path.exists')
    @patch('src.lib.gmail_functions.pickle.load')
    def test_get_creds_token_exists(self, mock_pickle_load, mock_path_exists):
        mock_path_exists.return_value = True
        mock_creds = MagicMock()
        mock_pickle_load.return_value = mock_creds
        
        
        creds = get_creds(main_dir_path + "/src/auth/Gmail/token.pickle")
        self.assertIsNotNone(creds)
        mock_pickle_load.assert_called_once()

    @patch('src.lib.gmail_functions.os.path.exists')
    @patch('src.lib.gmail_functions.pickle.load')
    def test_get_creds_no_token(self, mock_pickle_load, mock_path_exists):
        mock_path_exists.return_value = False
        
        creds = get_creds(main_dir_path + "/src/auth/Gmail/token.pickle")
        self.assertIsNone(creds)
        mock_pickle_load.assert_not_called()

    @patch('src.lib.gmail_functions.create_creds')
    @patch('src.lib.gmail_functions.get_creds')
    def test_check_creds(self, mock_get_creds, mock_create_creds):
        mock_creds = MagicMock()
        mock_get_creds.return_value = mock_creds
        
        creds = check_creds()
        self.assertIsNotNone(creds)
        mock_get_creds.assert_called_once()
        mock_create_creds.assert_not_called()

if __name__ == '__main__':
    unittest.main()
