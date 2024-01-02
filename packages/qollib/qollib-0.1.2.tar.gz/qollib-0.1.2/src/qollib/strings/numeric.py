import re
from functools import cmp_to_key

NUM_PATTERN = re.compile(r"\d+")


def sort_num(strings: list) -> list:
    """
    Applies a sorting algorithm to a list of strings containing an integer number.
    Selecting the first integer of the string and sort by it (regardless of zero-padded or not)
    """
    strings.sort(key=cmp_to_key(num_compare))
    return strings


def num_compare(string_a: str, string_b: str) -> int:
    start_a = extract_int(string_a)
    start_b = extract_int(string_b)
    if start_a > start_b:
        return 1
    if start_a == start_b:
        return 0
    return -1


def extract_int(string: str) -> int:
    """
    Extracts an integer from a string with a number.
    If multiple numbers, seperated by nun number characters, exist, the first one will be extracted.
    """
    matches = NUM_PATTERN.search(string)
    if not matches:
        return 0

    return int(matches.group())
