import socket
import sys
import pickle
import traceback
import time
from threading import Thread

startWork = False
endWork = False
totalThread = 0
count = 0
duty = {}

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

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):

    global startWork
    global endWork
    global count
    global totalThread
    global duty

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
            sendDuty = {"duty": duty["duty"][str(count)],
                        "result" : 0,
                        "quit": "no"}

            """
                Send duty to worker
            """
            connection.sendall(pickle.dumps(sendDuty))

            """
                Retrieved calculated result
            """
            afterWork = pickle.loads(connection.recv(5120))

            """
                Update general result
            """
            duty["result"] += afterWork["result"]

            """
                Number of worker
            """
            count += 1

            print("count : " , count , " totalThread : " , totalThread)

            print(afterWork)
            
            """
                Wait all worker thread to finish
            """
            while not endWork:
                time.sleep(0.1)
            startWork = False

    elif clientType == "I am master":

        print(clientType)

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
        connection.sendall(pickle.dumps(duty))

        """
            Set zero total worker's work
        """
        count = 0
        
        '''
        while is_active:
            client_input = receive_input(connection, max_buffer_size)

            if "--QUIT--" in client_input:
                print("Client is requesting to quit", flush=True)
                connection.close()
                print("Connection " + ip + ":" + port + " closed", flush=True)
                is_active = False
            else:
                print("Processed result: {}".format(client_input), flush=True)
                connection.sendall("-".encode("utf8"))
        '''

        
start_server()