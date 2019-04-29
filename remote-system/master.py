import socket
import pickle
import sys
import json

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    """
        Retrieved duty form user
    """
    # duty = {"duty": {"0": [1,2,33],
    #                  "1": [11,2,3,44,5,6,7,88,9],
    #                  "2": [12,2,33,4,55,6,77,8,99],
    #                  "3": [13,22,3,4,5,66,7,8,9]
    #                  },
    #         "type": "pow3",
    #         "result" : 0,
    #         "quit": "no"}


    """
        fill system config -- Normally you should construct systemconfig.json
    """
    with open('systemconfig.py') as json_file:
        duty = json.load(json_file)

    for i in duty["programs"]:
        with open("program_" + i + ".py") as program_file:  
            duty["programs"][i]["program"] = program_file.read()


    for i in duty["inputs"]:
        with open("inputs_" + i + ".txt") as inputs_file:  
            duty["inputs"][i] = inputs_file.read()
        # print (duty["inputs"][i])
        # print("---------------------- ------------------------")
    
    
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
    allResult = pickle.loads(soc.recv(5120))

    print(allResult)

if __name__ == "__main__":
    main()