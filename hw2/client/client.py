from socket import *

# Define the server's address and port
serverName = "localhost"  # The server will work on local machine
serverPort = 5050  # Choose an available port

# Create a TCP socket 
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverName, serverPort))

#upload or download
choice = input("Which operation to operate: upload or download? Response: u/d")

if choice == "u":#upload
    
    # Send the operation choice to server
    clientSocket.send("u".encode())

    # Open the file to be uploaded
    file = open("file.txt", "r")

    # Read the content of the file
    message = file.read()

    # Send the name of the file
    clientSocket.send("modified_file.txt".encode())

    # Send the contents
    clientSocket.send(message.encode())
    file.close()
    
    print("File uploaded to the server.")
    
elif choice == "d":#download
    # Send the operation choice to server
    clientSocket.send("d".encode())

    # Receive the filename
    filename = clientSocket.recv(1024).decode()

    # Open the file for writing transmitted file
    file = open(filename, "w")

    # Receive the content
    message = clientSocket.recv(1024).decode()

    file.write(message)
    file.close()

    # Open both files for comparison
    file = open(filename, "r")
    msg1 = file.read()
    original_file = open("file.txt", "r")
    msg2 = original_file.read()

    # comparison
    if msg1 == msg2:
        print("Successfully transmitted.")
    else:
        print("Unsuccessfully transmitted.")


    original_file.close()
    file.close()
else:#invalid input
    print("Wrong input, connect again!")

# Close the client socket
clientSocket.close()
