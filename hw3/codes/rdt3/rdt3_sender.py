import time

# Initial state
state = "WaitCall"

######################### Sender #########################

# Function to write a message to a file
def write_to_file(message, filename):
    with open(filename, 'a') as file:
        file.write(message + "\n")

# Function to create a packet with a given input string and sequence number
def make_pkt(input_string, seq_number):
    return str(seq_number), input_string

# Sender function simulating reliable data transfer
def rdt_send(seq_number):
    with open("gui_figure.txt", 'a') as file:
        file.write("rdt_send()\n")
    time.sleep(1)
    report(f"Packet {seq_number % 2} sent.")
    packet = make_pkt("Can Günyel", seq_number)
    udtSend(packet)

# Function to simulate the unreliable data transfer
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

    with open(filename, 'w') as file:
        file.write("")

    return message

# Main execution
if __name__ == "__main__":
    seq_number = -1

    while True:
        if state == "WaitCall":
            seq_number += 1
            rdt_send(seq_number)
            time.sleep(6)
            state = "WaitACK"
        else:
            with open("gui_input.txt", 'r') as file:
                input_value = file.read()
            with open("gui_input.txt", 'w') as file:
                pass
            if input_value == "lost":
                report(f"ACK {seq_number % 2} timed out.")
                rdt_send(seq_number)
                time.sleep(6)
                state = "WaitACK"
            elif input_value == "corrupt":
                report(f"NAK {seq_number % 2} received.")
                rdt_send(seq_number)
                time.sleep(6)
                state = "WaitACK"
            else:
                report(f"ACK {seq_number % 2} received.")
                state = "WaitCall"
