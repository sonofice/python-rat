#from socket import socket, AF_INET, SOCK_DGRAM
import socket, os
from getpass import getuser

port = 64780
host_IP = "127.0.0.1" # loopback

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host_IP, port))
    s.listen()
    print ("started listening")
    conn, addr = s.accept()

    with conn:
        while True:

            s.listen()
            print("listening")
            data = conn.recv(2048)
            print (data)
            cmnd = data.decode()
            print (str(cmnd))

            if str(cmnd.lower) == "exit":
                print("exiting")
                #cmnd = cmnd.encode()
                conn.sendall(cmnd)
                break
            elif str(cmnd.lower) == "listdir":
                result = os.path.dirname(os.path.realpath(__file__))
                print(result)  
            elif str(cmnd.lower) == "user":
                result = os.getlogin()
                print(result)
                
            else:
                result = "passing"

            conn.sendall(result.encode())