import socket
import threading
import os
import sys


def server_send(clientSocket, filename):
    # send the file to client
    pass


def handle_client(clientSocket, addr):

    clientSocket.send("Thank you for connecting".encode("utf-8"))
    while True:

        data = clientSocket.recv(1024)
        decoded_message = data.decode("utf-8")

        if decoded_message == "exit":
            print(f"Client {addr} disconnected")
            break

        if decoded_message.startswith("server_recieve"):

            # recieves the file from client

            file_name = decoded_message.split(" ")[1]
            filetodown = open("new" + file_name, "wb")
            while True:
                data = clientSocket.recv(1024)
                filetodown.write(data)
                ##checking for end of file
                if str(data)[-4:-1] == "EOF":
                    print("Done Receiving.")
                    break

            filetodown.close()
            print("STATUS: File Downloaded.")

            # clientSocket.close()

        if decoded_message.startswith("server_send"):
            file_name = decoded_message.split(" ")[1]
            # send the file to client

            filetoupload = open(file_name, "rb")
            data = filetoupload.read(1024)
            while data:
                clientSocket.send(data)
                data = filetoupload.read(1024)
            print("Done Sending.")
            print("STATUS: File Transfered.")

    clientSocket.close()


def main(port):

    # Create a socket object
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostbyname(socket.gethostname())
    serverSocket.bind((host, port))

    # Now wait for client connection.
    serverSocket.listen(5)
    print(f"SERVER STARTED Actively Listening on {host}:{port}")

    while True:
        # Establish connection with client.
        clientSocket, addr = serverSocket.accept()

        thread = threading.Thread(target=handle_client, args=(clientSocket, addr))
        thread.start()
        print(f"active connections {threading.active_count() - 1}")
        print("Got connection from", addr)


if __name__ == "__main__":
    main(5050)
