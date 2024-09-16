import sys
import os
import unittest
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
dir_name = os.path.dirname(dir_name)
main_dir_path = os.path.dirname(dir_name)
sys.path.append(main_dir_path)

from shift import Shift

def test_shift_creation(fixture_shift_V34):
    shift = Shift(
        name = fixture_shift_V34["name"],
        shift_id = fixture_shift_V34["shift_id"],
        start_time = fixture_shift_V34["start_time"],
        end_time = fixture_shift_V34["end_time"],
        description = fixture_shift_V34["description"],
    )

    assert shift.name == fixture_shift_V34["name"]
    assert shift.shift_id == fixture_shift_V34["shift_id"]
    assert shift.start_time == fixture_shift_V34["start_time"]
    assert shift.end_time == fixture_shift_V34["end_time"]
    assert shift.description == fixture_shift_V34["description"]

def test_shift_from_dict(fixture_shift_V34):
    shift = Shift.from_dict(fixture_shift_V34)

    assert shift.name == fixture_shift_V34["name"]
    assert shift.shift_id == fixture_shift_V34["shift_id"]
    assert shift.start_time == fixture_shift_V34["start_time"]
    assert shift.end_time == fixture_shift_V34["end_time"]
    assert shift.description == fixture_shift_V34["description"]

def test_shift_to_dict(fixture_shift_V34):
    shift = Shift.from_dict(fixture_shift_V34)
    assert shift.to_dict() == fixture_shift_V34

def test_shift_comparison(fixture_shift_V34):
    shift_1  = Shift.from_dict(fixture_shift_V34)
    shift_2  = Shift.from_dict(fixture_shift_V34)
    assert shift_1 == shift_2
