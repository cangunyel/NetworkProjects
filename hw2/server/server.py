from socket import *

# Define the port on which the server will listen 
serverPort = 5050

# Create a TCP socket 
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the server socket to IP address and port
serverSocket.bind(("", serverPort))

# Listen for incoming client connections
serverSocket.listen(1)
print("Server listening")


while True:
    # Accept a new connection
    connectionSocket, addr = serverSocket.accept()

    # Receive the operation choice
    operation = connectionSocket.recv(1024).decode()

    if operation == "u":#client upload server download
        

        # Receive the filename from the client
        filename = connectionSocket.recv(1024).decode()

        # Open the file for writing
        file = open(filename, "w")

        # Receive the contents
        message = connectionSocket.recv(1024).decode()

        # Write the received content to the file
        file.write(message)
        
        file.close()
        print("File downloaded from the client.")

    elif operation == "d":#client download server upload
        # Open the file for reading 
        file = open("modified_file.txt", "r")

        # Read the contents
        message = file.read()

        # Send the filename and contents
        connectionSocket.send("modified_file.txt".encode())
        connectionSocket.send(message.encode())

        file.close()
        print("File uploaded to the client")

    else:#undefined operation
        print("Undefined operation.")

    # Close the connection socket with the client
    connectionSocket.close()
