from resources.misc import sysinfo
from socket import socket, AF_INET, SOCK_STREAM
from os import listdir, getlogin, path

port = 64780
host_IP = "127.0.0.1"  # need to be loopback

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((host_IP, port))
    s.listen()
    print("started listening")
    conn, addr = s.accept()

    with conn:
        while True:

            s.listen()
            print("listening")
            data = conn.recv(2048)
            print(data)
            cmnd = data.decode()
            print(cmnd)

            if cmnd.lower() == "exit":
                print("exiting")
                break
            elif cmnd.lower() == "pwd":
                result = path.dirname(path.realpath(__file__))
            elif cmnd.lower() == "user":
                result = getlogin()
            elif cmnd.lower() == "listdir":
                result = listdir()
            elif cmnd.lower() == "sysinfo":
                result = sysinfo()
            else:
                result = "passing"

            conn.sendall(bytes(result, encoding="utf-8"))
