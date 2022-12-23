import pytest

from fast_json_pointer import rel_parser
from fast_json_pointer.exceptions import ParseException

def test_relative_parse_pointer():
    SERIALIZED_POINTER = "0"
    RELATIVE_RESPONSE = (0, [])

    relative_pointer = rel_parser.parse(SERIALIZED_POINTER)

    assert RELATIVE_RESPONSE == relative_pointer

def test_relative_parse_number_sign():
    SERIALIZED_POINTER = "0#"
    RELATIVE_RESPONSE = (0, None)

    relative_pointer = rel_parser.parse(SERIALIZED_POINTER)

    assert RELATIVE_RESPONSE == relative_pointer


def test_relative_parse_exceptions():
    POINTER = "-1"
    with pytest.raises(ParseException):
        # Negative integer
        relative_pointer = rel_parser.parse(POINTER)

    POINTER = "0.01"
    with pytest.raises(ParseException):
        # Floating point value
        relative_pointer = rel_parser.parse(POINTER)

    POINTER = "-0"
    with pytest.raises(ParseException):
        # Negative floating point value
        relative_pointer = rel_parser.parse(POINTER)

    POINTER = ""
    with pytest.raises(ParseException):
        # Empty string
        relative_pointer = rel_parser.parse(POINTER)

    POINTER = "#"
    with pytest.raises(ParseException):
        # Offset missing
        relative_pointer = rel_parser.parse(POINTER)

    POINTER = "0#/foo"
    with pytest.raises(ParseException):
        # Pointer cannot follow the number sign
        relative_pointer = rel_parser.parse(POINTER)


def test_relative_unparse_pointer():
    RELATIVE_POINTER = (0, ["foo"])
    SERIALIZED_RESPONSE = "0/foo"

    serialized_pointer = rel_parser.unparse(RELATIVE_POINTER)

    assert SERIALIZED_RESPONSE == serialized_pointer

def test_relative_unparse_number_sign():
    RELATIVE_POINTER = (0, None)
    SERIALIZED_RESPONSE = "0#"

    serialized_pointer = rel_parser.parse(RELATIVE_POINTER)

    assert SERIALIZED_RESPONSE == serialized_pointer
