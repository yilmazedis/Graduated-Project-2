import socket
import pickle
import sys
import json

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888


    """
        fill system config -- Normally you should construct systemconfig.json
    """
    with open('systemconfig.py') as json_file:
        duty = json.load(json_file)

    for i in duty["programs"]:
        with open("program_" + i + ".py") as program_file:  
            duty["programs"][i]["program"] = program_file.read()


    for i in duty["inputs"]:
        with open("inputs_" + i + ".txt", "rb") as inputs_file:  
            duty["inputs"][i] = list(inputs_file.read())
    

    #print( len(json.dumps(duty)))

    #exit()
    
    
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
    isSend = soc.recv(4096).decode("utf8")
    if isSend == "1":
        print("data Send")

    """
        Send duty to server
    """
    soc.sendall(pickle.dumps(duty))

    """
        Get result from server
    """
    
    allResult = {"progress": "-1"}
    while allResult["progress"] != '':
        allResult = pickle.loads(soc.recv(4096))
        print(allResult)
    
    # allResult = pickle.loads(soc.recv(4096))
    # print(allResult)

    allResult.pop("progress", None)
    
    for r in allResult:
        print(allResult[r]["filename"])
        print(pickle.loads(bytearray(allResult[r]["result"])))
    

if __name__ == "__main__":
    main()