# client

import time

################################### Receiver ##################################
# Function to handle the reception of a packet
def rdt_rcv(packet):
    with open("gui_figure.txt", "a") as file:
        file.write("rdt_rcv()" + "\n")

    with open("gui_input.txt", "r") as file:
        input = file.read()
        
    if input == "lost":
        return
        
     # Extract information from the received packet
    extract(packet)

# Function to extract data from a received packet
def extract(packet):
    data = packet.split()
    # Deliver FIN and send ACK/NAK 
    if data[0] == "Fin":
        deliver_data(data[0] + " " + data[1])
        time.sleep(0.5)
        ack_nak_send(data[0] + " " + data[1])

    # Deliver data and send ACK/NAK
    else:
        deliver_data(int(data[0]))
        time.sleep(0.5)
        ack_nak_send(int(data[0])+8)

# Function to deliver data based on the received packet
def deliver_data(data):

    report(f"Packet {data} received.")

# Function to read and erase content from a file
def read_and_erase_from_file(filename):
    with open(filename, "r") as file:
        message = file.read()

    # Erase the content of the file after reading
    with open(filename, "w") as file:
        file.write("")

    return message

############################################# Sender ################################

# Function to write a message to a file
def write_to_file(message, filename):
    with open(filename, "a") as file:

        file.write(message + "\n")

# Function to create a packet with a given input string and sequence number

def make_pkt(input_string, seq_number):
    return str(seq_number), input_string


def ack_nak_send(seq_number):
    with open("gui_input.txt", "r") as file:
        input = file.read()
    time.sleep(0.5)
    if input == "corrupt":
        report(f"NAK {seq_number} sent.")
        packet = make_pkt("NAK recieved", seq_number)
    else:
        report(f"ACK {seq_number} sent.")
        packet = make_pkt("ACK recieved", seq_number)
        # Log the delivery of data
    
    with open("gui_figure.txt", "a") as file:
        file.write("deliver_data()" + "\n")
    udtSend(packet)

# Function to simulate unreliable data transfer
def udtSend(packet):
    filename = "senderbuffer.txt"
    write_to_file(packet[0] + " " + packet[1], filename)

# Function to log a message
def report(message):
    with open("gui_file.txt", "a") as file:

        file.write(message + "\n")

# Sender function simulating reliable data transfer
def rdt_send(seq_number):

    time.sleep(1)
    # report(f"Packet {seq_number} sent.")
    packet = make_pkt("Can Günyel", seq_number)
    udtSend(packet)

# Function to start connection with a handshake request
def request_handshake(syn):
    filename = "senderbuffer.txt"
    write_to_file("Handshake Request", filename)


syn = 1
if __name__ == "__main__":
    request_handshake(syn)
    report(f"Handshake request with SYN={syn}.")
    while 1:
        time.sleep(1)
        handshake = read_and_erase_from_file("recieverbuffer.txt")
        if handshake.strip() == "Handshake Accepted":
            syn = 0
            time.sleep(2)
            report(f"Client acknowlegded connection. Changed SYN={syn}.")
            time.sleep(1)
            break

    while 1:

        received_message = read_and_erase_from_file("recieverbuffer.txt")
        time.sleep(1)
        if received_message:
            rdt_rcv(received_message)
            time.sleep(5)
