#from socket import socket, AF_INET, SOCK_DGRAM
import socket, os

# IP & port of the server



def run_connection():

    simple_cmd = ["listdir", "user", "systeminfo", "pwd", "upload", "download", "shell", "clear"]

    server_ip = "127.0.0.1" # replace with server IP
    port = 64780 # replace with server port

    # establish connection
    client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connection.connect((server_ip, port))

    while True:

       # input message
        user_input = str(input("Enter commands: "))

        # check if there is any input, if not break
        if user_input == "help":
            print ('''commands:
            listdir
            user
            systeminfo
            pwd
            upload
            download
            shell
            clear
            ''')
            continue

        elif user_input == "exit":
            client_connection.send(user_input.encode()[:2048])
            break
        elif user_input in simple_cmd:
            print("sending...")
        else:
            print ("No input was entered")
            os.system('cls' if os.name == 'nt' else 'clear')
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