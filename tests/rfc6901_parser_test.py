import pytest
from typing import List

from fast_json_pointer import rfc6901_parser
from fast_json_pointer.exceptions import ParseException


def test_parse():
    POINTER = "/foo/3/za"
    TOKENS = ["foo", "3", "za"]
    
    assert_parsed_pointer_against_tokens(POINTER, TOKENS)

def test_parse_escape_sequence_tilda():
    POINTER = "/foo/~0/za"
    TOKENS = ["foo", "~", "za"]
    
    assert_parsed_pointer_against_tokens(POINTER, TOKENS)

def test_parse_escape_sequence_solidus():
    POINTER = "/foo/~1/za"
    TOKENS = ["foo", "/", "za"]
    
    assert_parsed_pointer_against_tokens(POINTER, TOKENS)

def test_parse_escape_sequence_combined():
    POINTER = "/foo/~01/za"
    TOKENS = ["foo", "~1", "za"]
    
    assert_parsed_pointer_against_tokens(POINTER, TOKENS)

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
    TOKENS = ["foo", "3", "za"]
    POINTER = "/foo/3/za"
    
    assert_unparsed_tokens_against_pointer(TOKENS, POINTER)

def test_unparse_escape_sequence_tilda():
    TOKENS = ["foo", "~", "za"]
    POINTER = "/foo/~0/za"
    
    assert_unparsed_tokens_against_pointer(TOKENS, POINTER)

def test_unparse_escape_sequence_solidus():
    TOKENS = ["foo", "/", "za"]
    POINTER = "/foo/~1/za"
    
    assert_unparsed_tokens_against_pointer(TOKENS, POINTER)

def test_unparse_escape_sequence_combined():
    TOKENS = ["foo", "~1", "za"]
    POINTER = "/foo/~01/za"
    
    assert_unparsed_tokens_against_pointer(TOKENS, POINTER)


def assert_parsed_pointer_against_tokens(pointer: str, tokens: List[str])
    parsed = rfc6901_parser.parse(pointer)
    assert parsed == tokens

def assert_unparsed_tokens_against_pointer(tokens: List[str], pointer: str)
    unparsed = rfc6901_parser.unparse(tokens)
    assert unparsed == pointer