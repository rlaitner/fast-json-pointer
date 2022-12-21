from dataclasses import dataclass, field
from typing import *

from .pointer import JsonPointer, RelativeJsonPointer

from .exceptions import ResolutionException

JsonType = dict[str, "JsonType"] | list["JsonType"] | str | bool | int | float | None

@dataclass
class JsonRef:
    ref: JsonType
    pointer: JsonPointer


def _resolve_ref(doc: JsonType, part: str, base_pointer: JsonPointer) -> JsonRef:
    base_pointer = JsonPointer([*base_pointer.parts, part])

    match doc:
        case dict():
            if part not in doc:
                raise ResolutionException(f"Key '{part}' not in '{doc}' '{base_pointer}'")

            doc = doc[part]

        case list():
            part_idx = int(part)
            if part_idx >= len(doc):
                raise ResolutionException(f"Index '{part_idx}' not in '{doc}' '{base_pointer}'")

            doc = doc[part_idx]

        case _:
            raise ResolutionException(f"Unnvaigable doc type '{type(part)}' '{doc}' '{base_pointer}'")
    
    return JsonRef(doc, base_pointer)
                


def _resolve(doc: JsonType, parts: list[str], *, base_pointer: JsonPointer | None = None) -> list[JsonRef]:
    base_pointer = base_pointer or JsonPointer.parse("")
    doc_refs = [JsonRef(doc, base_pointer)]

    for part in parts:
        ref = _resolve_ref(doc, part, base_pointer)
        doc_refs.append(ref)
        doc = ref.ref
        base_pointer = ref.pointer

    return doc_refs


def get(doc: JsonType, pointer: JsonPointer, *, rel_pointer: RelativeJsonPointer | None = None) -> JsonType:
    '''
    
    >>> get({}, JsonPointer.parse(""))
    {}
    >>> get({'x': 5}, JsonPointer.parse("/x"))
    5
    >>> get({'x': {'': 3}}, JsonPointer.parse("/x/"))
    3
    >>> get({'x': {'': 3, 'z': 12}}, JsonPointer.parse("/x/"), rel_pointer=RelativeJsonPointer.parse("1/z"))
    12
    >>> get({'x': {'': 3}, 'z': 12}, JsonPointer.parse("/x/"), rel_pointer=RelativeJsonPointer.parse("1#"))
    'x'
    >>> get([{'x': {'': 3}}, 4], JsonPointer.parse("/0/x"), rel_pointer=RelativeJsonPointer.parse("1#"))
    '0'
    >>> get([{'x': {'': 3}}, 4], JsonPointer.parse("/0/x"), rel_pointer=RelativeJsonPointer.parse("0//does-not-exist"))
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ResolutionException: ...
    >>> get([{'x': {'': 3}}, 4], JsonPointer.parse("/3"))
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ResolutionException: ...
    >>> get([{'x': {'': 3}}, 4], JsonPointer.parse("/0/z"))
    Traceback (most recent call last):
    fast_json_pointer.exceptions.ResolutionException: ...
    '''
    doc_refs = _resolve(doc, pointer.parts)
    
    if rel_pointer:
        if rel_pointer.offset > 0:
            doc_refs = doc_refs[:-rel_pointer.offset]
        pointer = doc_refs[-1].pointer

        
        if rel_pointer.is_index_ref:
            return pointer.parts[-1]

        new_refs = _resolve(doc_refs[-1].ref, rel_pointer.parts, base_pointer=pointer)
        doc_refs.extend(new_refs)

    return doc_refs[-1].ref

def set(doc: JsonType, pointer: JsonPointer, value: JsonType, *, rel_pointer: RelativeJsonPointer | None = None) -> None:
    '''
    >>> x = {}
    >>> set(x, JsonPointer.parse("/x"), 2)
    >>> x
    {'x': 2}

    >>> x = {'x': 2}
    >>> set(x, JsonPointer.parse("/x"), 3, rel_pointer=RelativeJsonPointer.parse("1/y"))
    >>> x = {'x': 2, 'y': 3}
    '''
    doc_refs = _resolve(doc, pointer.parts[:-1])
    try:
        new_refs = _resolve_ref(doc_refs[-1].ref, pointer.parts[-1], base_pointer=doc_refs[-1].pointer)
        match doc_refs[-1].ref:
            case dict():
                doc_refs[-1].ref[pointer.parts[-1]] = value
            case list():
                doc_refs[-1].ref[int(pointer.parts[-1])] = value

    except ResolutionException:
        if rel_pointer is None:
            match doc_refs[-1].ref:
                    case dict():
                        doc_refs[-1].ref[pointer.parts[-1]] = value
                    case list():
                        doc_refs[-1].ref[int(pointer.parts[-1])] = value