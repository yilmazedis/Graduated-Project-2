import socket
import pickle
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    """
        Retrieved duty form user
    """
    duty = {"duty": {"0": [1,2,33],
                     "1": [11,2,3,44,5,6,7,88,9],
                     "2": [12,2,33,4,55,6,77,8,99],
                     "3": [13,22,3,4,5,66,7,8,9]
                     },

            "result" : 0,
            "quit": "no"}

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
    duty = pickle.loads(soc.recv(5120))

    print(duty)

if __name__ == "__main__":
    main()