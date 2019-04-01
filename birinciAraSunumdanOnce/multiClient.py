import socket
import pickle
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

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
        mList = duty["duty"]

        #------------------------------------------
        """
            !!! Beginning of calculation region !!!
        """
        #------------------------------------------


        result = sum(mList)



        #------------------------------------------
        """
            !!! End of calculation region !!!
        """
        #------------------------------------------

        """
            Construct json as result
        """
        duty["result"] = result

        """
            Send result
        """
        soc.sendall(pickle.dumps(duty))

    soc.close()
    print("Client is closed")

if __name__ == "__main__":
    main()