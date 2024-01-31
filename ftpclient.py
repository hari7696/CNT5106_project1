import socket
import time

def main(port):

    client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    print("CONNECTION ESTABLISHED WITH SERVER {} ON PORT {}".format(host, port))
    client.connect((host, port))
    print("server connection establiashed")

    while True:
        
        command = input("Enter command: ")
        

        if command.startswith('exit'):
            client.send('exit'.encode('utf-8'))
            client.shutdown(2)
            client.close()
            break
            
        elif command.startswith('upload'):
            file_name = command.split(' ')[1]
            
            #upload file to server
            client.send(f'server_recieve {file_name}'.encode('utf-8'))

            filetoupload = open(file_name, "rb")
            data = filetoupload.read(1024)
            while data:

                client.send(data)
                data = filetoupload.read(1024)
            filetoupload.close()
            print("Done Sending.")

        elif command.startswith('download'):
            file_name = command.split(' ')[1]
            # download filename.txt
            client.send(f'server_send {file_name}'.encode('utf-8'))
            filetodown = open('new' + file_name, "wb")
            while True:
                data = client.recv(1024)
                filetodown.write(data)
                if str(data)[-4:-1] == "EOF":
                    print("Done Receiving.")
                    break
                
            filetodown.close()
            print("File Downloaded.")


        else:
            print("Invalid command entered, please choose from following [upload filename, download filename, exit]")




if __name__ == '__main__':
    main(5050)  