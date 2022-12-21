import pytest

from fast_json_pointer import rfc6901_parser
from fast_json_pointer.exceptions import ParseException


def test_parse():
    parsed = rfc6901_parser.parse("/foo/3/za")
    assert parsed == ["foo", "3", "za"]


def test_parse_exceptions():

    with pytest.raises(ParseException):
        # No leading /
        rfc6901_parser.parse("foo/3/za")

    with pytest.raises(ParseException):
        # trailing ~
        rfc6901_parser.parse("/foo/3/za~")

    with pytest.raises(ParseException):
        # ~ not part of escape sequence
        rfc6901_parser.parse("/fo~o/3/za")

    with pytest.raises(ParseException):
        # ~ with invalid int
        rfc6901_parser.parse("/foo/~3/za")


def test_unparse():
    unparsed = rfc6901_parser.unparse(["foo", "3", "za"])
    assert unparsed == "/foo/3/za"
