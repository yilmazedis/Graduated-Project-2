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
    subprocess.run(['python3', 'program.py'], stdout=subprocess.PIPE)

def c_code():
    pass

def cpp_code():
    pass

def java_code():
    pass

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

        print("Recieved Duty : \n" , duty)

        """
            Get data that should process
        """
        #getInput = duty["input"]

        

        #------------------------------------------
        """
            !!! Beginning of calculation region !!!
        """
        #------------------------------------------

        print(duty)
        for code in duty["programs"]:
            
            if duty["programs"][code]["language"] == "python":

                add_python_libraries(duty["programs"][code]["libraries"])

                with open("program.py", "w") as program_file:  
                    program_file.write(duty["programs"][code]["program"])

                # python_code()

            elif duty["programs"][code]["language"] == "c":
                c_code()
            elif duty["programs"][code]["language"] == "cpp":
                cpp_code()
            elif duty["programs"][code]["language"] == "java":
                java_code()

            # os.remove("program.py")

        
        result["result"] = 1


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