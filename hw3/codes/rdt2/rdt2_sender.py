import time 

# Initial state for the sender
state = "WaitCall"

######################### Sender #########################

# Function to write a message to a file
def write_to_file(message, filename):
    with open(filename, 'a') as file:
        file.write(message + "\n")

# Function to create a packet with sequence number and input string
def make_pkt(input_string, seq_number):
    return str(seq_number), input_string
    
# Function to perform reliable data transfer (rdt_send)
def rdt_send(seq_number):
    with open("gui_figure.txt", 'a') as file:
        file.write("rdt_send()\n")
    time.sleep(1)  # Simulated delay
    report(f"Packet {seq_number} sent.")
    packet = make_pkt("Can Günyel", seq_number)
    udtSend(packet)

# Function to simulate the unreliable channel (udt_send)
def udtSend(packet):
    with open("gui_figure.txt", 'a') as file:
       file.write("udt_send()\n")   
    filename = "recieverbuffer.txt"
    write_to_file(packet[0] + ' ' + packet[1], filename)

# Function to log a message
def report(message):
    with open("gui_file.txt", 'a') as file:
        file.write(message + "\n")

######################### Reader #########################


# Function to read and erase content from a file
def read_and_erase_from_file(filename):
    with open(filename, 'r') as file:
        message = file.read()

    # Erase the content of the file after reading
    with open(filename, 'w') as file:
        file.write("")

    return message

# Main execution
if __name__ == "__main__":
    seq_number = 0

    while True:
        if state == "WaitCall":
            seq_number += 1
            # Perform reliable data transfer
            rdt_send(seq_number)
            time.sleep(6)  # Simulated delay before sending the next packet
            state = "WaitACK"
        else:
            with open("gui_input.txt", 'r') as file:
                input = file.read()
            with open("gui_input.txt", 'w') as file:
                pass
            # received_message = read_and_erase_from_file("senderbuffer.txt")
            if input == "corrupt":
                report(f"NAK {seq_number} received.")  
                # Resend the packet and wait for acknowledgment
                rdt_send(seq_number)
                time.sleep(6)
                state = "WaitACK"
            else:
                report(f"ACK {seq_number} received.")  
                # Process the acknowledgment and go back to the "WaitCall" state
                state = "WaitCall"
