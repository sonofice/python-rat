#from socket import socket, AF_INET, SOCK_DGRAM
import socket

port = 64780
host_IP = "127.0.0.1" # loopback

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host_IP, port))
    s.listen()
    print ("started listening")
    conn, addr = s.accept()

    with conn:
        while True:

            try:
                s.listen()
                print("listening")
                data = conn.recv(2048)
                cmnd = data.decode()

                if cmnd == "exit":
                    print("exiting")
                    break

                print ("interrupted")


                cmnd = cmnd.encode()
                conn.sendall(cmnd)
            except cmnd.socketerror("interruptedfakka"):
                break

