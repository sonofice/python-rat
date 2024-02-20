import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while(True):
        msg = input("Your command: ")
        s.sendall(str.encode(msg))
        if(msg == "exit"):
            print("Bye")
            break
        data = s.recv(2048)
        print("Received: ", data.decode())