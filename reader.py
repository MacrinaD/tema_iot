"""
componenta centrala a "consumatorului"
sursa: https://www.eadan.net/blog/ipc-with-named-pipes/
"""
import os
import select
import struct


def decode_value_len(size: bytes) -> int:
    return struct.unpack('<I', size)[0]


def decode_value(value: bytes) -> float:
    return struct.unpack('f', value)[0]


def process_bytes(reader: int) -> float:
    size_bytes = os.read(reader, 4)
    value_bytes = os.read(reader, decode_value_len(size_bytes))
    return decode_value(value_bytes)


if __name__ == '__main__':
    FIFO_NAME = '/tmp/comm'

    os.mkfifo(path=FIFO_NAME, mode=0o600)

    try:
        reader_endpoint = os.open(FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)
        try:
            sampler = select.poll()
            sampler.register(reader_endpoint, select.POLLIN)
            try:
                while True:
                    if (reader_endpoint, select.POLLIN) in sampler.poll(2000):
                        temp_value = process_bytes(reader_endpoint)
                        print('Am primit: {0}'.format(temp_value))
                    else:
                        print("Nobody here :(")
            except KeyboardInterrupt as kbd_ex:
                print('Closing reader... ')
            finally:
                sampler.unregister(reader_endpoint)
        finally:
            os.close(reader_endpoint)
    finally:
        os.remove(FIFO_NAME)
        print('Exiting...')
