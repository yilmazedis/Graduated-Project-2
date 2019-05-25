from flask import Flask, flash, request, redirect, url_for
import os
import json
from flask_cors import CORS
import socket
import sys
import pickle



duty = {}
duty["programs"] = {}
duty["inputs"] = {}

p_counter = 0
i_counter = 0
l_counter = 0

t_process = 0

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

    print(json.dumps(duty, indent=4, sort_keys=True))

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
    soc.sendall("I am master".encode("utf8"))

    """
        Verify if everyting ok
    """
    isSend = soc.recv(5120).decode("utf8")
    if isSend == "1":
        print("data Send")

    """
        Send duty to server
    """
    soc.sendall(pickle.dumps(duty))

    """
        Get result from server
    """
    progressTime = 1
    allResult = {"progress": "-1"}
    while allResult["progress"] != '':
        allResult = pickle.loads(soc.recv(5120))
        if allResult["progress"] != '':

            t_process += int(100 / (p_counter * i_counter))
        else:
            t_process = 100

        print(t_process)
    
    # allResult = pickle.loads(soc.recv(5120))
    # print(allResult)

    allResult.pop("progress", None)
    
    for r in allResult:
        print(allResult[r]["filename"])
        print(pickle.loads(bytearray(allResult[r]["result"])))


    duty = {}
    duty["programs"] = {}
    duty["inputs"] = {}

    p_counter = 0
    i_counter = 0
    l_counter = 0


    soc.close()

    return '200'


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
    data = file.read().decode("utf-8")

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
    print(file.filename)
    
    filename = file.filename



    file.seek(0)
    data = list(file.read())

    duty["inputs"][str(i_counter)] = {}

    duty["inputs"][str(i_counter)] = data
    i_counter += 1

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
            
