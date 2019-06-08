import socket
import pickle
import sys
import os
import subprocess
import json
import copy

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

def pipInstall(package):
    os.system('pip3 install ' + package)

def add_python_libraries(libraries):
    if libraries != "":
        for lib in eval(libraries):
            if lib not in sys.modules:
                pipInstall(lib)
                print(lib + " is installed!")
            else:
                print(lib + " have already installed!")

def python_code():
    p = subprocess.Popen(['python3', 'program.py'])
    p.wait()

def c_code():
    subprocess.run(['gcc', '-o', 'prog', 'program.c'], stdout=subprocess.PIPE)
    p = subprocess.Popen(['./prog'])
    p.wait()

def cpp_code():
    subprocess.run(['g++', '-o', 'prog', 'program.cpp'], stdout=subprocess.PIPE)
    p = subprocess.Popen(['./prog'])
    p.wait()

def java_code():
    subprocess.run(['javac', 'program.java'], stdout=subprocess.PIPE)
    p = subprocess.Popen(['java', 'program'])
    p.wait()

def clisp_code():
    p = subprocess.Popen(['clisp', 'program.lisp'])
    p.wait()

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    result = {}

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    power = {"whois": "I am worker", "power": 10}
    mySend(soc, pickle.dumps(power))

    print("power: " ,power["power"])

    while True:
        """
            Recieve duty
        """
        duty = pickle.loads(myReceive(soc))

        # print(duty)

        """
            Check Should worker close
        """
        if duty["quit"] == "yes":
            print("Client is closing...")
            break

        # print("Recieved Duty : \n" , duty)

        """
            Get data that should process
        """
        #getInput = duty["input"]

        #------------------------------------------
        """
            !!! Beginning of calculation region !!!
        """
        #------------------------------------------

        # print(duty)
        mock = {"mock": 0}
        programInput = duty["input"]

        with open("inputs", "wb") as f:
            f.write(programInput)

        for code in duty["programs"]:
            
            if duty["programs"][code]["language"] == "py":

                add_python_libraries(duty["programs"][code]["libraries"])

                with open("program.py", "wb") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                python_code()

            elif duty["programs"][code]["language"] == "c":

                with open("program.c", "wb") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                c_code()

            elif duty["programs"][code]["language"] == "cpp":

                with open("program.cpp", "wb") as program_file:  
                    program_file.write(duty["programs"][code]["program"])
                
                cpp_code()

            elif duty["programs"][code]["language"] == "java":

                with open("program.java", "wb") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                java_code()

            elif duty["programs"][code]["language"] == "lisp":

                with open("program.lisp", "wb") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                clisp_code()

            mySend(soc, pickle.dumps({"progress": code}))
            mock = pickle.loads(myReceive(soc))
            # os.remove("program.py")

        direc = os.listdir(".")

        byte = 0

        outputFileName = ""

        for o in direc:
            if("outputs" == o):
                outputFileName = o 
                with open(o, "rb") as f:
                    bytesList = f.read()
        
        result["result"] = bytesList
        result["filename"] = outputFileName
        result["progress"] = ""


        for o in direc:
            if("outputs" in o):
                os.remove(o)
            if "prog" == o or "inputs" == o or "program" in o:
                os.remove(o)


        #------------------------------------------
        """
            !!! End of calculation region !!!
        """
        #------------------------------------------

        """
            Send result
        """
        mySend(soc, pickle.dumps(result))

        #print(len(json.dumps(result)))

    soc.close()
    print("Client is closed")

if __name__ == "__main__":
    main()