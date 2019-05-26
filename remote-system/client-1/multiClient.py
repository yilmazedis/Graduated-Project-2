import socket
import pickle
import sys
import os
import subprocess

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

    soc.sendall("I am worker".encode("utf8"))

    while True:
        """
            Recieve duty
        """
        duty = pickle.loads(soc.recv(5120))

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

        programInput = duty["input"]

        with open("inputs", "wb") as f:
            f.write(bytearray(programInput))

        for code in duty["programs"]:
            
            if duty["programs"][code]["language"] == "py":

                add_python_libraries(duty["programs"][code]["libraries"])

                with open("program.py", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                python_code()

            elif duty["programs"][code]["language"] == "c":

                with open("program.c", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                c_code()

            elif duty["programs"][code]["language"] == "cpp":

                with open("program.cpp", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])
                
                cpp_code()

            elif duty["programs"][code]["language"] == "java":

                with open("program.java", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                java_code()

            elif duty["programs"][code]["language"] == "clisp":

                with open("program.lisp", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                clisp_code()

            soc.sendall(pickle.dumps({"progress": code}))
            # os.remove("program.py")

        direc = os.listdir(".")

        byte = 0

        outputFileName = ""

        for o in direc:
            if("outputs" in o):
                outputFileName = "2" + o
                with open(o, "rb") as f:
                    bytesList = list(f.read())
        
        result["result"] = bytesList
        result["filename"] = outputFileName
        result["progress"] = ""

        for o in direc:
            if("outputs" in o):
                os.remove(o)
        #------------------------------------------
        """
            !!! End of calculation region !!!
        """
        #------------------------------------------

        """
            Send result
        """
        soc.sendall(pickle.dumps(result))

    soc.close()
    print("Client is closed")

if __name__ == "__main__":
    main()