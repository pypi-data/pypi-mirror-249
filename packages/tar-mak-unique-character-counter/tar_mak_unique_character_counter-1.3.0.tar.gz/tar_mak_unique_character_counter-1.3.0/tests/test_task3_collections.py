from src.tar_mak_unique_character_counter.task3_collections import count_unique_chars, main
import pytest
from unittest.mock import patch


@pytest.fixture
def temp_file(tmp_path):
    data = "qwe"
    temp_file = tmp_path / "temp.txt"
    temp_file.write_text(data)
    return temp_file


def test_main_with_string_argument(capsys):
    test_args = ['main.py', '--string', "qwe"]
    with patch('sys.argv', test_args):
        main()
    captured = capsys.readouterr()
    assert "3" in captured.out


def test_main_with_file_argument(capsys, temp_file):
    test_args = ['main.py', '--file', str(temp_file)]
    with patch('sys.argv', test_args):
        main()
    captured = capsys.readouterr()
    assert "3" in captured.out


def test_return_character_number():
    assert count_unique_chars("abbbccdf") == 3


def test_appropriate_data_type():
    with pytest.raises(TypeError):
        count_unique_chars([])
