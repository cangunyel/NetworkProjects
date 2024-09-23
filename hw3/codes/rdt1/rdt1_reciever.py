import time

################################### Receiver ##################################

# Function to handle the reception of a packet
def rdt_rcv(packet):
    with open("gui_figure.txt", 'a') as file:
        file.write("rdt_rcv()\n") 
       
    with open("gui_input.txt", 'r') as file:
        input_value = file.read()
  
    # Extract information from the received packet
    extract(packet)

# Function to extract data from a received packet
def extract(packet):
    data = packet.split()
    # Deliver data
    deliver_data(data)

# Function to deliver data based on the received packet
def deliver_data(data):
    # Log the received packet
    report(f"Packet {data[0]} received.")
    time.sleep(1)  # Simulated delay
    with open("gui_figure.txt", 'a') as file:
        file.write("deliver_data()\n")   

# Function to read and erase content from a file
def read_and_erase_from_file(filename):
    with open(filename, 'r') as file:
        message = file.read()

    # Erase the content of the file after reading
    with open(filename, 'w') as file:
        file.write("")

    return message

# Function to log a message
def report(message):
    with open("gui_file.txt", 'a') as file:
        file.write(message + "\n")

# Main execution
if __name__ == "__main__":
    while True:
        # Read and erase content from the receiver buffer
        received_message = read_and_erase_from_file("recieverbuffer.txt")
        if received_message:
            # Process the received message
            rdt_rcv(received_message)

        time.sleep(6)  # Simulated delay before checking for new messages again
