import socket
import sys
import pickle
import traceback
import time
import json
from threading import Thread , Lock
import copy
import math

startWork = False
endWork = False
totalThread = 0
count = 0
duty = {}
allResult = {}
masterConnection = 0
mutex = Lock()
allPower = 0
powerList = []
getAllInputs = False
filtered = {}

def start_server():
    host = ''
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    th_id = 0
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        
        try:
            Thread(target=client_thread, args=(connection, ip, port, th_id)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

        th_id += 1

    soc.close()


def client_thread(connection, ip, port, th_id, max_buffer_size = 4096):

    global startWork
    global endWork
    global count
    global totalThread
    global duty
    global allResult
    global masterConnection
    global allPower
    global powerList
    global getAllInputs
    global filtered

    threadAction = "YES"

    clientType = pickle.loads(myReceive(connection))

    
    if clientType["whois"] == "I am worker":

        """
            construct shared inputs json
        """
        filtered[str(th_id)] = {}

        
        power = clientType["power"]

        """
            All power
        """
        allPower += power

        print("power ", power)

        """
            add power to list
        """
        powerList.append(power)

        """
            Counter total ready workers
        """
        totalThread += 1
        
        print(clientType)

        while True:
            print(threadAction)
            
            getAllInputs = False

            """
                Verify if duty is started
            """
            while not startWork:
                time.sleep(0.1)
            endWork = False

            """
                Proper duty to process
            """
            
            
            if len(duty["inputs"]) >= th_id + 1:

                totalInputs = len(duty["inputs"])

                # share
                if totalInputs > totalThread:

                    
                    runSharedInputs = True

                    if th_id == 0:           

                        """
                            Beginning Of Input Share Part
                        """
                        hak = []
                        for p in powerList:
                            hak.append(math.ceil((p * totalInputs) / allPower))

                        print("hak: ", hak)
                        print("sum of hak: ", sum(hak))

                        sortedHak = copy.deepcopy(hak)

                        sortedHak = sorted(hak,reverse=True)

                        print("sorted Hak: ", sortedHak)

                         
                        sortedIndex = sorted(range(len(hak)), reverse=True, key=hak.__getitem__)

                        while sum(sortedHak) != totalInputs:
                            for i in range(len(hak)):
                                if sortedHak[i] != 1 and sum(sortedHak) != totalInputs:
                                    sortedHak[i] -= 1

                        print("modified sortedHak: ", sortedHak)
                        print("sum of modified sortedHak: ", sum(sortedHak))
                        print("sortedIndex: ", sortedIndex)

                        actualCase = [y for y, x in sorted(zip(sortedHak, sortedIndex))]

                        print("actual case: ", actualCase)

                        preKey = "0"
                        actualIndex = 1

                        for share in actualCase:
                            keys = [str(key) for key in range(int(preKey), int(share) + int(preKey) )]
                            filtered[str(actualIndex - 1)] = dict(zip(keys, [duty["inputs"][str(k)] for k in keys]))
                            preKey = sum(actualCase[0:actualIndex])
                            print(filtered[str(actualIndex - 1)])
                            print()
                            actualIndex += 1
                            

                        """
                            End Of Input Share Part
                        """

                        getAllInputs = True
                    


                else:
                    runSharedInputs = False
                    """
                        Send duty to worker
                    """

                print("basla ", th_id)
                while getAllInputs == False and th_id != 0:
                    pass
                print("bitti ", th_id)

                inputsIndex = 0
                workerKeys = list(filtered[str(th_id)].keys())
                print("workerKeys list", workerKeys)
                while inputsIndex < len(workerKeys) or not runSharedInputs:
                    
                    if not runSharedInputs:

                        mySend(connection, pickle.dumps({"input": duty["inputs"][str(th_id)],
                                                        "programs": duty["programs"],
                                                        "quit": "no"}))
                        
                        inputsIndex = len(filtered)
                        print("input az")
                        runSharedInputs = True # finish process
                    else:
                        print("th ", th_id ,workerKeys[inputsIndex])
                        
                        mySend(connection, pickle.dumps({"input": filtered[str(th_id)][workerKeys[inputsIndex]],
                                                        "programs": duty["programs"],
                                                        "quit": "no"}))
                        
                    
                    """
                        Retrieved calculated result
                    """
                    mock = {"mock": 0}
                    afterWork = {"progress": "-1"}
                    while afterWork["progress"] != "":
                        mutex.acquire()

                        afterWork = pickle.loads(myReceive(connection))
                        if afterWork["progress"] != "":
                            mySend(connection, pickle.dumps(mock))
                        
                        print(afterWork)
                        if afterWork["progress"] != "":
                            
                            mySend(masterConnection, pickle.dumps(afterWork))
                            mock = pickle.loads(myReceive(masterConnection))

                        mutex.release()

                    mutex.acquire()
                    """
                        Update general result
                    """

                    allResult[workerKeys[inputsIndex]] = copy.deepcopy(afterWork)
                    print("Thread id : ", th_id)
                    """
                        Number of worker
                    """
                    mutex.release()

                    inputsIndex += 1
                

                # print("count : " , count , " totalThread : " , totalThread)

                # print(afterWork)
                
                """
                    Wait all worker thread to finish
                """
            count += 1
            while not endWork:
                time.sleep(0.1)
            startWork = False

    elif clientType["whois"] == "I am master":

        print(clientType)

        masterConnection = connection

        """
            Verify if master side active
        """
        mySend(connection, "1".encode("utf8"))

        """
            Retrieve all duty from user to process
        """

        duty = pickle.loads(myReceive(connection))

        """
            Start work and wait unitl finish all
        """
        startWork = True
        while count != totalThread:
            time.sleep(0.1)
        
        """
            End of workers work.
        """
        endWork = True

        """
            Send all Retrieved result to user.
        """
        print("result send")
        allResult["progress"] = ""
        mySend(connection, pickle.dumps(allResult))

        """
            Set zero total worker's work
        """
        count = 0


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
        
start_server()