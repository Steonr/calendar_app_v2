import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from src.main import main

class TestMain(unittest.TestCase):

    @patch('src.main.setup_logging')
    @patch('src.main.check_creds')
    @patch('src.main.give_dir')
    def test_main(self, mock_give_dir, mock_check_creds, mock_setup_logging):
        mock_give_dir.return_value = None
        mock_check_creds.return_value = True

        main()

        mock_setup_logging.assert_called_once()
        mock_check_creds.assert_called_once()

if __name__ == '__main__':
    unittest.main()
