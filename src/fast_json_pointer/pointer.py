from __future__ import annotations
from dataclasses import dataclass
from typing import *

from . import rfc6901_parser, rel_parser

class _ReprStrMixin:
    def __repr__(self) -> str:
        # inner single quotes is consistent w/ how str.__repr__ works
        return f"{type(self).__name__}('{str(self)}')"



@dataclass(repr=False)
class JsonPointer(_ReprStrMixin):
    '''Primitive dataclass for RFC 6901 json pointers.
    
    >>> JsonPointer(['~home', 'foo.txt', 'mime/type'])
    JsonPointer('/~0home/foo.txt/mime~1type')
    >>> JsonPointer.parse('/~0home/foo.txt/mime~1type')
    JsonPointer('/~0home/foo.txt/mime~1type')
    '''
    parts: list[str]
    '''Unescaped list of path parts.
    
    >>> JsonPointer.parse("/data/items/0/id").parts
    ['data', 'items', '0', 'id']
    '''

    def __str__(self) -> str:
        '''Serialize to RFC 6901 json pointer.
        '''
        return rfc6901_parser.unparse(self.parts)

    @classmethod
    def parse(cls, s: str) -> Self:
        '''Parse a serialized RFC 6901 json pointer.
        '''
        return cls(parts=rfc6901_parser.parse(s))

    # I dediced against this, as it's nagged at me since I first wrote it that you should't
    # resolve JSON pointers w/o having a Doccument you're resolving them across.
    #
    #def join(self, other: JsonPointer | RelativeJsonPointer | str) -> Self:
    #    match other:
    #        case JsonPointer(parts):
    #            return type(self)(parts=[*self.parts, *parts])
    #
    #        case str():
    #            return type(self)(parts=[*self.parts, other])
    #
    #        case RelativeJsonPointer(offset, pointer):
    #            remaining = len(self.parts) - offset
    #            if remaining < 0:
    #                raise PathJoiningException(
    #                    "Tried to ascend past root of json doc when appending relative pointer"
    #                )
    #            our_parts = self.parts[:remaining]
    #            their_parts = [] if pointer is None else pointer.parts
    #
    #            return type(self)(parts=[*our_parts, *their_parts])
       



@dataclass(repr=False)
class RelativeJsonPointer((_ReprStrMixin)):
    '''Primitive data class for 2020-12 draft json pointers.

    >>> RelativeJsonPointer(0, JsonPointer(['data', 'items']))
    RelativeJsonPointer('0/data/items')

    >>> RelativeJsonPointer(0, None)
    RelativeJsonPointer('0#')
    '''
    # https://json-schema.org/draft/2019-09/relative-json-pointer.html
    offset: int
    pointer: JsonPointer | None
    
    @property
    def parts(self) -> list[str] | None:
        '''Unescaped list of path parts, if this isn't an index reference.
        
        >>> RelativeJsonPointer.parse("0/data/items/0/id").parts
        ['data', 'items', '0', 'id']
        >>> RelativeJsonPointer.parse("0#").parts is None
        True
        '''
        return None if self.pointer is None else self.pointer.parts

    @property
    def is_index_ref(self) -> bool:
        '''
        >>> RelativeJsonPointer.parse("0").is_index_ref
        False
        >>> RelativeJsonPointer.parse("0/").is_index_ref
        False
        >>> RelativeJsonPointer.parse("0#").is_index_ref
        True
        '''
        return self.pointer is None

    def __str__(self) -> str:
        '''Serialize to 2020-12 draft relative json pointer.
        '''
        return rel_parser.unparse(self.offset, self.parts)

    @classmethod
    def parse(cls, s: str) -> Self:
        '''Parse a serialized 2020-12 draft relative json pointer.
        '''
        offset, parts = rel_parser.parse(s)
        return cls(offset=offset, pointer=None if parts is None else JsonPointer(parts=parts))