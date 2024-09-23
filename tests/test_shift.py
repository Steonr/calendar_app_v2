import uuid
import unittest
from datetime import datetime
from dotenv import load_dotenv
from src.domain.entities.shift import Shift
from src.domain.value_objects import ShiftId
# Load environment variables from .env file
load_dotenv()
class TestShift(unittest.TestCase):

    def setUp(self):
        # This method is called before every test. Initialize common variables here.
        self.shift_data = {
            'shift_id': uuid.uuid4(),
            'name': 'Morning Shift',
            'start_time': datetime(2024, 9, 17, 9, 0),
            'end_time': datetime(2024, 9, 17, 17, 0),
            'description': 'Shift from 9 AM to 5 PM'
        }

    def test_create_shift_from_dict(self):
        # Test creation of Shift object from dictionary
        shift = Shift.from_dict(self.shift_data)
        self.assertEqual(shift.name, 'Morning Shift')
        self.assertEqual(shift.start_time, datetime(2024, 9, 17, 9, 0))
        self.assertEqual(shift.end_time, datetime(2024, 9, 17, 17, 0))
        self.assertEqual(shift.description, 'Shift from 9 AM to 5 PM')
        self.assertIsInstance(shift.shift_id, ShiftId)

    def test_shift_to_dict(self):
        # Test conversion of Shift object to dictionary
        shift = Shift.from_dict(self.shift_data)
        shift_dict = shift.to_dict()
        self.assertEqual(shift_dict['name'], 'Morning Shift')
        self.assertEqual(shift_dict['start_time'], datetime(2024, 9, 17, 9, 0))
        self.assertEqual(shift_dict['end_time'], datetime(2024, 9, 17, 17, 0))
        self.assertEqual(shift_dict['description'], 'Shift from 9 AM to 5 PM')
        self.assertEqual(shift_dict['shift_id'], self.shift_data['shift_id'])

    def test_invalid_shift_id(self):
        # Test that invalid ShiftId raises an error
        invalid_data = self.shift_data.copy()
        invalid_data['shift_id'] = 'invalid_uuid'
        with self.assertRaises(ValueError):
            Shift.from_dict(invalid_data)

if __name__ == '__main__':
    unittest.main()
