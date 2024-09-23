import time

################################### Receiver ##################################

# Function to handle the reception of a packet
def rdt_rcv(packet):
    with open("gui_figure.txt", 'a') as file:
        file.write("rdt_rcv()\n") 
        
    with open("gui_input.txt", 'r') as file:
        input_value = file.read()
    
    # If the input is "lost," do nothing
    if input_value == "lost":
        return
  
    # Extract information from the received packet
    extract(packet)

# Function to extract data from a received packet
def extract(packet):
    data = packet.split()
    # Deliver data and send ACK/NAK
    deliver_data(data)
    ack_nak_send(data[0])

# Function to deliver data based on the received packet
def deliver_data(data):
    # Log the received packet
    report(f"Packet {int(data[0]) % 2} received.")

# Function to read and erase content from a file
def read_and_erase_from_file(filename):
    with open(filename, 'r') as file:
        message = file.read()

    # Erase the content of the file after reading
    with open(filename, 'w') as file:
        file.write("")

    return message

############################################# Sender ################################

# Function to write a message to a file
def write_to_file(message, filename):
    with open(filename, 'a') as file:
        file.write(message + "\n")

# Function to create a packet with a given input string and sequence number
def make_pkt(input_string, seq_number):
    return str(seq_number), input_string

# Function to send ACK or NAK based on input condition
def ack_nak_send(seq_number):
    with open("gui_input.txt", 'r') as file:
        input_value = file.read()
    
    time.sleep(1)
    
    if input_value == "corrupt":
        report(f"NAK {int(seq_number) % 2} sent.")  
        packet = make_pkt("NAK received", seq_number)
    else:
        report(f"ACK {int(seq_number) % 2} sent.")
        packet = make_pkt("ACK received", seq_number)
    
    # Log the delivery of data
    with open("gui_figure.txt", 'a') as file:
       file.write("deliver_data()\n")     
    udtSend(packet)

# Function to simulate unreliable data transfer
def udtSend(packet):
    filename = "senderbuffer.txt"
    write_to_file(packet[0] + ' ' + packet[1], filename)

# Function to log a message
def report(message):
    with open("gui_file.txt", 'a') as file:
        file.write(message + "\n")

# Main execution
if __name__ == "__main__":
    while True:
        # Read and erase content from the receiver buffer
        received_message = read_and_erase_from_file("recieverbuffer.txt")
        time.sleep(1)  # Simulated delay before checking for messages
        
        if received_message:
            # Process the received message
            rdt_rcv(received_message)
        else:
            # No message found, continue waiting
            pass
        
        # Simulated delay before checking for new messages again
        time.sleep(5)
