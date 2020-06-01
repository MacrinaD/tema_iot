"""
componenta centrala a "producatorului"
sursa: https://www.eadan.net/blog/ipc-with-named-pipes/
"""
import os
import random
import struct
import time
from message_encoder import create_msg


def read_temp() -> float:
    temp_value = random.random() * 10
    return temp_value


if __name__ == '__main__':
    FIFO_NAME = "/tmp/comm"

    fifo_writer = os.open(FIFO_NAME, os.O_WRONLY)

    try:
        while True:
            time.sleep(2)
            read_value = read_temp()
            print('Trimit: {0}'.format(read_value))
            message = create_msg(bytearray(struct.pack('f', read_value)))
            os.write(fifo_writer, message)
    except KeyboardInterrupt as kdb_ex:
        print('Closing...')
    finally:
        os.close(fifo_writer)
