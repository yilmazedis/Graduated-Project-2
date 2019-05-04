import socket
import sys
import pickle
import traceback
import time
import json
from threading import Thread

startWork = False
endWork = False
totalThread = 0
count = 0
duty = {}
allResult = {}
masterConnection = 0

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


def client_thread(connection, ip, port, th_id, max_buffer_size = 5120):

    global startWork
    global endWork
    global count
    global totalThread
    global duty
    global allResult
    global masterConnection

    threadAction = "YES"

    clientType = connection.recv(5120).decode("utf8")

    if clientType == "I am worker":

        """
            Counter total ready workers
        """
        totalThread += 1
        
        print(clientType)

        while True:
            print(threadAction)
            
            """
                Verify if duty is started
            """
            while not startWork:
                time.sleep(0.1)
            endWork = False

            """
                Proper duty to process
            """
            

            """
                Send duty to worker
            """
            connection.sendall(pickle.dumps({"input": duty["inputs"][str(th_id)],
                                            "programs": duty["programs"],
                                            "quit": "no"}))

            """
                Retrieved calculated result
            """
            afterWork = {"progress": "-1"}
            while afterWork["progress"] != "":
                afterWork = pickle.loads(connection.recv(5120))
                print(afterWork)
                if afterWork["progress"] != "":
                    masterConnection.sendall(pickle.dumps(afterWork))

            """
                Update general result
            """
            allResult[str(th_id)] = json.loads(json.dumps(afterWork))

            """
                Number of worker
            """
            count += 1

            # print("count : " , count , " totalThread : " , totalThread)

            # print(afterWork)
            
            """
                Wait all worker thread to finish
            """
            while not endWork:
                time.sleep(0.1)
            startWork = False

    elif clientType == "I am master":

        print(clientType)

        masterConnection = connection

        """
            Verify if master side active
        """
        connection.sendall("1".encode("utf8"))

        """
            Retrieve all duty from user to process
        """
        duty = pickle.loads(connection.recv(5120))

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
        allResult["progress"] = ""
        connection.sendall(pickle.dumps(allResult))

        """
            Set zero total worker's work
        """
        count = 0
        
start_server()