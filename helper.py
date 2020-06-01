import struct
import os
import random


def decode_value_len(size: bytes) -> int:
    return struct.unpack('<I', size)[0]


def decode_value(value: bytes) -> float:
    return struct.unpack('f', value)[0]


def process_bytes(reader: int):
    size_bytes = os.read(reader, 4)
    value_bytes = os.read(reader, decode_value_len(size_bytes))
    return value_bytes


def read_temp() -> float:
    temp_value = random.random() * 10
    return temp_value