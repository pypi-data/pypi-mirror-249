from collections import Counter
from functools import lru_cache
import argparse
from pathlib import Path


@lru_cache
def count_unique_chars(data: str) -> int:
    """

    :param data: the string in which the characters should be counted
    :return: number of characters in the data occurring only once
    """
    if not isinstance(data, str):
        raise TypeError(f"expected string, got {type(data)}")
    return len([char for char, times in Counter(data).items() if times == 1])


def read_from_file(filepath: str) -> str:
    """
    This function read file and return symbols occurring only once
    :param filepath: path to the file
    :return:
    """
    with open(Path(filepath), 'r') as fp:
        return fp.read()


def main():
    """
    This function creates CLI for return_single_characters function

    """
    parser = argparse.ArgumentParser(description="This application returns characters occurring in data only once")
    parser.add_argument('--string', '-s', type=str, help="enter your data", default=None)
    parser.add_argument('--file', "-f", help="enter file path", default=None)
    args = parser.parse_args()
    if args.file is None and args.string is None:
        print("Please enter at least one argument")
    text = read_from_file(args.file) if args.file else args.string
    print(count_unique_chars(text))


if __name__ == "__main__":
    main()
