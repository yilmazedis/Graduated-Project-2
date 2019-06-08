from flask import Flask, flash, request, redirect, url_for, jsonify, Response, send_file
import os
import json
from flask_cors import CORS
import socket
import sys
import pickle
import copy
from io import BytesIO
from zipfile import ZipFile 
import time

forResponse = {}
duty = {}
duty["programs"] = {}
duty["inputs"] = {}

p_counter = 0
i_counter = 0
l_counter = 0

t_process = 0

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res

def myReceive(sock):
    socksize = 1024

    size = sock.recv(4) # assuming that the size won't be bigger then 1GB
    size = bytes_to_number(size)
    current_size = 0
    myBuffer = b""
    while current_size < size:
        data = sock.recv(socksize)
        if not data:
            break
        if len(data) + current_size > size:
            data = data[:size-current_size] # trim additional data
        myBuffer += data
        # you can stream here to disk
        current_size += len(data)
    return myBuffer

def mySend(sock, data):
    length = len(data)
    sock.send(convert_to_bytes(length)) # has to be 4 bytes
    byte = 0
    while byte < length:
        sock.send(data[byte:byte+1024])
        byte += 1024

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    
    global duty

    print(json.dumps(duty, indent=4, sort_keys=True))


    p_counter = 0
    i_counter = 0
    l_counter = 0

    return 'Hello, World!'

@app.route('/download')
def download ():
    """
    for item in forResponse:
        for item["result"]

    file_like_object = io.BytesIO(my_zip_data)
    zipfile_ob = zipfile.ZipFile(file_like_object)
    """

    return jsonify(forResponse)

@app.route('/process')
def traceProcess ():

    global t_process

    #t_process += 1



    return str(t_process)

@app.route('/start', methods=["POST"])
def start():

    global duty
    global p_counter
    global i_counter
    global l_counter
    global t_process
    global forResponse



    # print(json.dumps(duty, indent=4, sort_keys=True))

    print("Process Started")

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    t_process = 0

    try:
        soc.connect((host, port))      
    except:
        print("Connection error")
        sys.exit()

    """
        Talk server as master
    """
    power = {"whois": "I am master", "power": 0}
    mySend(soc, pickle.dumps(power))

    """
        Verify if everyting ok
    """
    isSend = myReceive(soc).decode("utf8")
    if isSend == "1":
        print("data Send")

    """
        Send duty to server
    """
    mySend(soc, pickle.dumps(duty))
    mock = {"mock": 0}
    """
        Get result from server
    """
    progressTime = 1
    allResult = {"progress": "-1"}
    while allResult["progress"] != '':
        allResult = pickle.loads(myReceive(soc))
        mySend(soc, pickle.dumps(mock))
        if allResult["progress"] != '':

            t_process += 100 / (p_counter * i_counter)
        else:
            t_process = 100

        print(t_process)

    allResult.pop("progress", None)

    for r in allResult:
        allResult[r]["filename"] = r + "_" + allResult[r]["filename"]

    for r in allResult:
        print(allResult[r]["filename"])
    
    if i_counter < len(allResult):
        print("inputs ", i_counter, "allResult: ", len(allResult))
        for i in range(len(allResult)):
            if i >= i_counter:
                allResult.pop(str(i), None)


    forResponse = copy.deepcopy(allResult)

    duty = {}
    duty["inputs"] = {}
    duty["programs"] = {}

    p_counter = 0
    i_counter = 0
    l_counter = 0

    print(duty)


    soc.close()

    return "200"


@app.route('/program', methods=["POST"])
def program_files():

    print("program")

    global duty
    global p_counter
    global i_counter
    global l_counter

    file = request.files['file']
    print(file.filename)
    
    filename = file.filename
    file.seek(0)
    data = file.read()

    duty["programs"][str(p_counter)] = {}


    duty["programs"][str(p_counter)]["program"] = data
    duty["programs"][str(p_counter)]["language"] = filename.split('.')[-1]
    duty["programs"][str(p_counter)]["libraries"] = ""

    p_counter += 1

    print(data)
    #file.save(os.path.join("./", filename))

    return "200"

@app.route('/input', methods=["POST"])
def input_files():

    global duty
    global p_counter
    global i_counter
    global l_counter
    print("input")

    file = request.files['file']
    
    
    filename = file.filename



    file.seek(0)
    data = file.read()

    if filename.split('.')[-1] == "zip":
        with ZipFile(BytesIO(data)) as my_zip_file:
            for contained_file in my_zip_file.namelist():
                # with open(("unzipped_and_read_" + contained_file + ".file"), "wb") as output:
                rawdata = b''
                for line in my_zip_file.open(contained_file).readlines():
                    
                    rawdata += line
                duty["inputs"][str(i_counter)] = rawdata
                print("rawdata : ", rawdata)
                i_counter += 1
    else:
        duty["inputs"][str(i_counter)] = data
        i_counter += 1

    # duty["inputs"][str(i_counter)] = {}

    print(duty["inputs"])
    
    print(file.filename)
    print(data)
    #file.save(os.path.join("./", filename))

    return "200"

@app.route('/library', methods=["POST"])
def library_files():

    global duty
    global p_counter
    global i_counter
    global l_counter

    print("library")

    file = request.files['file']
    print(file.filename)
    
    filename = file.filename
    file.seek(0)
    data = file.read().decode("utf-8")


    duty["programs"][str(l_counter)]["libraries"] = data 

    print(data)
    #file.save(os.path.join("./", filename))

    return "200"
            
