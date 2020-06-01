import os
import select

from helper import process_bytes


class Pipes:
    FIFO_REQUEST = '/tmp/sensor'
    FIFO_ANSWER = '/tmp/sensor_answer'

    def __init__(self):
        self.__received_data = None
        self.killthreads = False

    def get_received_data(self):
        return self.__received_data

    def kill_all_threads(self):
        self.killthreads = True

    def write_to_pipe(self, endpoint, message):
        os.write(endpoint, message)

    def connect_to_pipe(self, pipe_name):
        fifo_writer = os.open(pipe_name, os.O_WRONLY)
        return fifo_writer

    def listening_pipe(self, pipe_name):
        os.mkfifo(path=pipe_name, mode=0o600)
        value_was_received = False

        try:
            sensor_data = os.open(pipe_name, os.O_RDONLY | os.O_NONBLOCK)
            try:
                sampler = select.poll()
                sampler.register(sensor_data, select.POLLIN)
                try:
                    while not self.killthreads and not value_was_received:
                        if (sensor_data, select.POLLIN) in sampler.poll(2000):
                            temp_value = process_bytes(sensor_data)
                            self.__received_data = temp_value
                            value_was_received = True

                            print('Am primit: {0}'.format(temp_value))

                except KeyboardInterrupt as kbd_ex:
                    print('Closing reader... ')
                    self.kill_all_threads()

                finally:
                    sampler.unregister(sensor_data)
            finally:

                os.close(sensor_data)
        finally:
            os.remove(pipe_name)
            print('Exiting...')

