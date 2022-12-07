import re
from typing import *

from .exceptions import ParseException

RE_INVALID_ESCAPE = re.compile("(~[^01]|~$)")


def validate(s: str) -> None:
    if match := RE_INVALID_ESCAPE.search(s):
        raise ParseException("Found invalid escape {}".format(match.group()))


def parse(s: str) -> list[str]:
    validate(s)

    parts = s.split("/")
    # discard "empty" str, as "/foo/bar" becomes ["", "foo", "bar"]
    if parts.pop(0) != "":
        raise ParseException("JSON pointers must start with /")
    return [unescape(p) for p in parts]


def unparse(parts: Iterable[str]) -> str:
    return "/" + "/".join(escape(part) for part in parts)


def escape(s: str) -> str:
    # Escape `~` first! https://www.rfc-editor.org/rfc/rfc6901#section-4
    return s.replace("~", "~0").replace("/", "~1")


def unescape(s: str) -> str:
    # Unscape `~` last! https://www.rfc-editor.org/rfc/rfc6901#section-4
    return s.replace("~1", "/").replace("~0", "~")
