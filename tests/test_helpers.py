import unittest
import os
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
main_dir_path = os.path.dirname(dir_name)
from src.helpers.helpers import give_dir, setup_logging

class TestHelpers(unittest.TestCase):

    def test_give_dir_current(self):
        current_file = __file__
        expected_dir = os.path.dirname(current_file)
        self.assertEqual(give_dir(current_file), expected_dir)

    def test_give_dir_level_up(self):
        current_file = __file__
        expected_dir = os.path.dirname(os.path.dirname(current_file))
        self.assertEqual(give_dir(current_file, 1), expected_dir)

    def test_setup_logging(self):
        # Check if log file is created
        setup_logging()
        log_file_path = give_dir(__file__, 2)
        print("log file path", give_dir(__file__, 2))
        self.assertTrue(os.path.exists(log_file_path))

if __name__ == '__main__':
    unittest.main()