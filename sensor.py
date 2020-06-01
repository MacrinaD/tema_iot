"""
componenta centrala a "consumatorului"
sursa: https://www.eadan.net/blog/ipc-with-named-pipes/
"""
from pipes import Pipes
from threading import Thread
from message_encoder import create_msg
from helper import read_temp_senzor1

import struct

if __name__ == '__main__':
    FIFO_NAME = Pipes.FIFO_REQUEST
    my_reader_pipe = Pipes()
    while my_reader_pipe.killthreads is False:
        try:
            my_thread = Thread(target=my_reader_pipe.listening_pipe, args=(FIFO_NAME, ))
            my_thread.start()
            my_thread.join()

            print(my_reader_pipe.get_received_data())

            writer_endpoint = my_reader_pipe.connect_to_pipe(Pipes.FIFO_ANSWER)
            my_reader_pipe.write_to_pipe(writer_endpoint, message=create_msg(bytearray(struct.pack('f', read_temp_senzor1()))))

        except KeyboardInterrupt as kbd_ex:
            print('Closing reader... ')
            my_reader_pipe.kill_all_threads()
        finally:
            pass

    FIFO_NAME = Pipes.FIFO_REQUEST
    my_reader_pipe = Pipes()
    while my_reader_pipe.killthreads is False:
        try:
            my_thread = Thread(target=my_reader_pipe.listening_pipe, args=(FIFO_NAME,))
            my_thread.start()
            my_thread.join()

            print(my_reader_pipe.get_received_data())

            writer_endpoint = my_reader_pipe.connect_to_pipe(Pipes.FIFO_ANSWER)
            my_reader_pipe.write_to_pipe(writer_endpoint, message=create_msg(bytearray(struct.pack('f', read_temp_senzor2()))))

        except KeyboardInterrupt as kbd_ex:
            print('Closing reader... ')
            my_reader_pipe.kill_all_threads()
        finally:
            pass
