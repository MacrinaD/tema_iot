from flask import Flask
from flask import abort, request
from flask import jsonify, make_response
from message_encoder import create_msg
from threading import Thread
import glob
import os
import logging
import threading
import time
from pipes import Pipes
from helper import decode_value


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/directory3', methods=['GET'])
def get_files_from_sensor_configuration():
    files = glob.glob("./sensor_configuration/*")
    response = []
    for file in files:
        response.append(os.path.basename(file))
    return response


@app.route('/api/directory3/<sensorName>', methods=['GET'])
def get_data_from_sensor(sensorName):
    FIFO_NAME = Pipes.FIFO_REQUEST
    FIFO_NAME_ANSWER = Pipes.FIFO_ANSWER
    my_answer_pipe = Pipes()

    fifo_writer = os.open(FIFO_NAME, os.O_WRONLY)
    ret_val = "NOK", 400

    try:
        my_answer_thread = Thread(target=my_answer_pipe.listening_pipe, args=(FIFO_NAME_ANSWER, ))
        my_answer_thread.start()
        message = create_msg(b"Hello sensor")
        os.write(fifo_writer, message)
        my_answer_thread.join()
        my_answer_pipe.kill_all_threads()
        ret_val = jsonify({"message": str(decode_value(my_answer_pipe.get_received_data()))})
    except KeyboardInterrupt as kdb_ex:
        print('Closing...')
    finally:
        os.close(fifo_writer)
    return ret_val


@app.route('/api/directory/<senzor_name>', methods=['POST'])
def post_data_to_sens_configuration(senzor_name):
    file = './sensor_configuration/' + senzor_name + "_config.txt"
    print(file)
    data = request.get_data()
    print(data)
    if os.path.exists(file) is False:
        os.mknod(file)
    else:
        return "Bad Request", 400

    if not data or len(data) == 0:
        return "NOK", 204

    file = open(file, 'w')
    file.write(data.decode('ascii'))
    file.close()
    return "OK"


@app.route('/api/<senzor_name>/celsius', methods=['PUT'])
def update_config_celsius(senzor_name):
    config_file_name = "./sensor_configuration/" + senzor_name + "_config.txt"
    if os.path.exists(config_file_name) is False:
        return "Fisierul de configurare pentru senzor nu exista.", 204

    else:

        file = open(config_file_name, 'w')
        file.write("celsius")
        file.close()
        return "OK"


@app.route('/api/<senzor_name>/fahrenheit', methods=['PUT'])
def update_config_Fahrenheit(senzor_name):
    config_file_name = "./sensor_configuration/" + senzor_name + "_config.txt"
    if os.path.exists(config_file_name) is False:
        return "Fisierul de configurare pentru senzor nu exista.", 204

    else:

        file = open(config_file_name, 'w')
        file.write("fahrenheit")
        file.close()
        return "OK"


@app.route('/api/<senzor_name>/kelvin', methods=['PUT'])
def update_config_kelvin(senzor_name):
    config_file_name = "./sensor_configuration/" + senzor_name + "_config.txt"
    if os.path.exists(config_file_name) is False:
        return "Fisierul de configurare pentru senzor nu exista.", 204

    else:

        file = open(config_file_name, 'w')
        file.write("kelvin")
        file.close()
        return "OK"


@app.route('/api/directory', methods=['GET'])
def get_files_from_files_lab1():
    files = glob.glob("./files_lab1/*")
    response = []
    for file in files:
        response.append(os.path.basename(file))
    return response


@app.route('/api/directory2', methods=['GET'])
def get_files_from_empdb():
    files = glob.glob("./empdb/*")
    response = []
    for file in files:
        response.append(os.path.basename(file))
    return response


@app.route('/api/directory2/<fileName>', methods=['GET'])
def get_file_contents_from_empdb(fileName):
    response = get_files_from_empdb()

    print(fileName)
    if fileName in response:
        file_to_read = open(glob.glob("./empdb/" + fileName)[0])
        response = file_to_read.read()
        file_to_read.close()
    else:
        abort(404)
    print(response)
    return response


@app.route('/api/directory/<fileName>', methods=['PUT'])
def create_or_replace(fileName):
    files = get_files_from_files_lab1()
    filename_path = ''
    if fileName in files:
        return "NOK", 204
    else:
        filename_path = './files_lab1/' + fileName
        os.mknod(filename_path)

    return "File " + filename_path + " created", 201


@app.route('/api/directory2/<fileName>', methods=['PUT'])
def create_or_replace_in_empdb(fileName):
    files = get_files_from_empdb()
    filename_path = ''
    if fileName in files:
        return "NOK", 204
    else:
        filename_path = './empdb/' + fileName
        os.mknod(filename_path)

    return "File " + filename_path + " created", 201


@app.route('/api/directory/<fileName>', methods=['DELETE'])
def delete_file_from_lab1_files(fileName):
    file = './files_lab1/'+fileName
    if os.path.exists(file) is True:
        os.remove(file)
        return "OK"
    else:
        return "File not found", 204


@app.route('/api/directory2/<fileName>', methods=['DELETE'])
def delete_file_from_empdb(fileName):
    file = './empdb/'+fileName
    if os.path.exists(file) is True:
        os.remove(file)
        return "OK"
    else:
        return "File not found", 204


@app.route('/api/directory/<fileName>', methods=['POST'])
def post_data_to_lab1_files(fileName):
    file = './files_lab1/' + fileName
    print(file)
    data = request.get_data()
    print (data)

    if not data or len(data) == 0:
        return "No content", 204

    if os.path.exists(file) is False:
        os.mknod(file)

    file = open(file, 'w+')
    file.write(data.decode('ascii'))
    file.close()
    return "OK"


@app.route('/api/directory2/<fileName>', methods=['POST'])
def post_data_to_emp_file(fileName):
    file = './empdb/' + fileName
    print(file)
    data = request.get_data()
    print (data)

    if not data or len(data) == 0:
        return "No content", 204

    if os.path.exists(file) is False:
        os.mknod(file)

    file = open(file, 'w+')
    file.write(data.decode('ascii'))
    file.close()
    return "OK"


@app.route('/api/directory', methods=['GET'])
def display_files_from_empdb():
    files = glob.glob("./files_lab1/*")
    response = dict()
    count = 1
    for file in files:
        response[count] = file
        count = count + 1

    return response


@app.route('/api/directory2', methods=['GET'])
def display_files_from_lab1():
    files = glob.glob("./empdb/*")
    response = dict()
    count = 1
    for file in files:
        response[count] = file
        count = count + 1

    return response


@app.route('/api/directory2/employee', methods=['GET'])
def getAllEmp():

    return jsonify({'emp': empDB})

empDB=[

 {

 'id':'101',

 'name':'Saravanan S',

 'title':'Technical Leader'

 },

 {

 'id':'201',

 'name':'Rajkumar P',

 'title':'Sr Software Engineer'

 }

 ]
if __name__ == "__main__":


    app.run()
