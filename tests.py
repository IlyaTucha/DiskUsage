from unittest.mock import patch
from Filters import Filters
import datetime
import pytest
from DiskUsageCalculator import DiskUsageCalculator

def test_get_file_size_for_file():
    calculator = DiskUsageCalculator("test_directory")
    size = calculator.get_file_size("tests/2/NvLowLatencyVk.dll")
    assert size == 48952

def test_get_file_size_for_directory():
    calculator = DiskUsageCalculator("tests")
    size = calculator.get_file_size("tests")
    assert size == 2306464

def test_format_size():
    calculator = DiskUsageCalculator("tests")
    formatted_size = calculator.convert_size(1024, "KB")
    assert formatted_size == "1 KB"

@pytest.fixture(params=[('', None), ('.dll', '.dll')])
def extension_filter_input(request):
    with patch('builtins.input', side_effect=[request.param[0]]):
        yield request.param

def test_get_extension_filter_input(extension_filter_input):
    result = Filters.get_extension_filter_input()
    expected_result = extension_filter_input[1]
    assert result == expected_result

@pytest.fixture(params=[('15-09-2023', datetime.date(2023, 9, 15)), ('', None)])
def date_filter_input(request):
    with patch('builtins.input', side_effect=[request.param[0]]):
        yield request.param

def test_get_date_filter_input(date_filter_input):
    result = Filters.get_date_filter_input()
    expected_result = date_filter_input[1]
    assert result == expected_result

@pytest.fixture(params=[('2', 2), ('', None)])
def max_depth_input(request):
    with patch('builtins.input', side_effect=[request.param[0]]):
        yield request.param

def test_get_max_depth_input(max_depth_input):
    result = Filters.get_max_depth_input()
    expected_result = max_depth_input[1]
    assert result == expected_result

if __name__ == "__main__":
    pytest.main()