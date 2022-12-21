"""Implements releative json pointer parsing. See `2020-12 relative json
pointer draft <https://json-schema.org/draft/2020-12/relative-json-pointer.html>`_ for
the (draft) specification.
"""

import re
from typing import Iterable

from . import rfc6901_parser
from .exceptions import ParseException

RE_NONNEG_INT = re.compile("0|[1-9][0-9]*")


def parse(s: str) -> tuple[int, list[str] | None]:
    """Parse a relative json pointer into :code:`tuple[offset, parts | None]`.

    If parts aren't returned it's due to the pointer containing a ``#`` operator at
    it's tail, and thus being an "index / name of" reference.

    :raises: :exc:`.ParseException`: If relative json pointer is invalid.

    An offset by itself is valid.

    >>> parse("0") # Points at self
    (0, [])
    >>> parse("1") # Points at parent
    (1, [])
    >>> parse("2") # Points at grandparent
    (2, [])


    Only non-negative integers are valid offsets.

    >>> parse("-1")
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    >>> parse("-0") # Even negative zero
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...


    An offset must always be provided, an empty string **isn't** valid.

    >>> parse("")
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...


    An offset can be followed by ``#`` to imply the index or name of the referenced
    object should be returned, rather than it's value.

    >>> parse("0#")
    (0, None)
    >>> parse("2#")
    (2, None)


    ``#`` is *also* a valid character in a json pointer, there are a few ways to
    write relative pointers that break first-glance intuition.

    >>> parse("0/#")
    (0, ['#'])
    >>> parse("0/#/foo")
    (0, ['#', 'foo'])
    >>> parse("0/foo#")
    (0, ['foo#'])
    >>> parse("0/foo/#")
    (0, ['foo', '#'])


    ``#`` without an offset is invalid.

    >>> parse('#')
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...


    ``#`` **must not** be followed with a json pointer, or any other text.

    >>> parse("0#/foo")
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    >>> parse("#im_not_a_pointer")
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ParseException: ...
    """
    match = RE_NONNEG_INT.match(s)

    if not match:
        raise ParseException("Relative json-pointer must begin with non-neg int")

    offset = int(match.group())
    rest = s[match.end() :]

    if rest.startswith("#"):
        if len(rest) > 1:
            raise ParseException("Relative json-pointer has symbols after #")
        return offset, None
    else:
        return offset, rfc6901_parser.parse(rest)


def unparse(offset: int, parts: Iterable[str] | None) -> str:
    """Serialize a relative json pointer.

    >>> unparse(0, ["foo"])
    '0/foo'
    >>> unparse(0, None)
    '0#'
    >>> unparse(0, [])
    '0'
    >>> unparse(0, ['#'])
    '0/#'
    >>> unparse(0, ["foo#"])
    '0/foo#'
    """
    return f"{offset}{'#' if parts is None else rfc6901_parser.unparse(parts)}"
