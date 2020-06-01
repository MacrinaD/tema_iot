import struct
import os
import random
import glob



def decode_value_len(size: bytes) -> int:
    return struct.unpack('<I', size)[0]


def decode_value(value: bytes) -> float:
    return struct.unpack('f', value)[0]


def process_bytes(reader: int):
    size_bytes = os.read(reader, 4)
    value_bytes = os.read(reader, decode_value_len(size_bytes))
    return value_bytes


def read_temp_senzor1() -> float:
    temp_c = random.random() * 10
    path_to_file = glob.glob('./sensor_configuration/senzor_temperatura1_config.txt')[0]
    f = open(path_to_file, "r")
    scale = f.readline()
    if 'kelvin' in scale:
        temp_c = temp_c - 273.15
    elif 'fahrenheit':
        temp_c = temp_c * 9 / 5 + 32
    return temp_c









