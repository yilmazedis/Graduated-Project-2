from flask import Flask, flash, request, redirect, url_for
import os
import json

duty = {}
duty["programs"] = {}
duty["inputs"] = {}

p_counter = 0
i_counter = 0
l_counter = 0

t_download = -1

app = Flask(__name__)

@app.route('/')
def hello():
    
    global duty

    print(json.dumps(duty, indent=4, sort_keys=True))


    p_counter = 0
    i_counter = 0
    l_counter = 0

    return 'Hello, World!'

@app.route('/download', methods=["GET"])
def downloadFile ():

    global t_download

    t_download += 1



    return str(t_download)

@app.route('/start', methods=["POST"])
def start():

    global duty
    global p_counter
    global i_counter
    global l_counter

    print(json.dumps(duty, indent=4, sort_keys=True))

    duty = {}
    duty["programs"] = {}
    duty["inputs"] = {}

    p_counter = 0
    i_counter = 0
    l_counter = 0

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
    data = file.read().decode("utf-8")

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
            
