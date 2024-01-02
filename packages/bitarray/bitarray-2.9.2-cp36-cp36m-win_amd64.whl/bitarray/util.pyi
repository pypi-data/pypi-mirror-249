# Copyright (c) 2021 - 2024, Ilan Schnell; All Rights Reserved

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from typing import Any, AnyStr, BinaryIO, Optional, Union

from bitarray import bitarray, BytesLike, CodeDict


FreqMap = Union[Counter[int], dict[Any, Union[int, float]]]


def zeros(length: int, endian: Optional[str] = ...) -> bitarray: ...
def ones(length: int, endian: Optional[str] = ...) -> bitarray: ...

def urandom(length: int, endian: Optional[str] = ...) -> bitarray: ...
def pprint(a: Any, stream: BinaryIO = ...,
           group: int = ...,
           indent: int = ...,
           width: int = ...) -> None: ...

def make_endian(a: bitarray, endian: str) -> bitarray: ...
def rindex(a: bitarray,
           sub_bitarray: Union[bitarray, int] = ...,
           start: int = ...,
           stop: int = ...) -> int: ...

def strip(a: bitarray, mode: str = ...) -> bitarray: ...

def count_n(a: bitarray,
            n: int,
            value: int = ...) -> int: ...

def parity(a: bitarray) -> int: ...
def count_and(a: bitarray, b: bitarray) -> int: ...
def count_or(a: bitarray, b: bitarray) -> int: ...
def count_xor(a: bitarray, b: bitarray) -> int: ...
def any_and(a: bitarray, b: bitarray) -> bool: ...
def subset(a: bitarray, b: bitarray) -> bool: ...
def _correspond_all(a: bitarray, b: bitarray) -> tuple: ...

def intervals(a: bitarray) -> Iterator: ...

def ba2hex(a: bitarray) -> str: ...
def hex2ba(s: AnyStr, endian: Optional[str] = ...) -> bitarray: ...
def ba2base(n: int, a: bitarray) -> str: ...
def base2ba(n: int,
            s: AnyStr,
            endian: Optional[str] = ...) -> bitarray: ...

def ba2int(a: bitarray, signed: int = ...) -> int: ...
def int2ba(i: int,
           length: int = ...,
           endian: str = ...,
           signed: int = ...) -> bitarray: ...

def serialize(a: bitarray) -> bytes: ...
def deserialize(b: BytesLike) -> bitarray: ...
def sc_encode(a: bitarray) -> bytes: ...
def sc_decode(stream: BytesLike) -> bitarray: ...
def vl_encode(a: bitarray) -> bytes: ...
def vl_decode(stream: BytesLike,
              endian: Optional[str] = ...) -> bitarray: ...

def _huffman_tree(freq_map: FreqMap) -> Any: ...
def huffman_code(freq_map: FreqMap,
                 endian: Optional[str] = ...) -> CodeDict: ...
def canonical_huffman(Freq_Map) -> tuple[CodeDict, list, list]: ...
def canonical_decode(a: bitarray,
                     count: Sequence[int],
                     symbol: Iterable[Any]) -> Iterator: ...
