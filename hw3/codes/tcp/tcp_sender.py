# server
finish = 0
import time

state = "WaitCall"
#########################sender##########################
def write_to_file(message, filename):
    with open(filename, "a") as file:

        file.write(message + "\n")

# Function to create a packet with a given input string and sequence number
def make_pkt(input_string, seq_number):
    return str(seq_number), input_string

# Sender function simulating reliable data transfer
def rdt_send(seq_number):
    with open("gui_figure.txt", "a") as file:
        file.write("rdt_send()\n")
    time.sleep(1)
    report(f"Packet {seq_number} sent.")
    packet = make_pkt("Can Günyel", seq_number)
    udtSend(packet)

# Function to simulate the unreliable data transfer
def udtSend(packet):
    with open("gui_figure.txt", "a") as file:
        file.write("udt_send()" + "\n")
    filename = "recieverbuffer.txt"
    write_to_file(packet[0] + " " + packet[1], filename)

# Function to log a message
def report(message):
    with open("gui_file.txt", "a") as file:

        file.write(message + "\n")


######################### Reader #########################



# Function to read and erase content from a file
def read_and_erase_from_file(filename):
    with open(filename, "r") as file:
        message = file.read()

    # Erase the content of the file after reading
    with open(filename, "w") as file:
        file.write("")

    return message

# Function to start connection with a handshake accept
def accept_handshake(syn):
    filename = "recieverbuffer.txt"
    write_to_file("Handshake Accepted", filename)


if __name__ == "__main__":
    syn = 1
    while 1:
        time.sleep(1)
        handshake = read_and_erase_from_file("senderbuffer.txt")
        if handshake.strip() == "Handshake Request":
            time.sleep(3)
            report(f"Handshake accepted with SYN={syn}.")

            accept_handshake(syn)
            time.sleep(3)
            syn = 0
            break
    seq_number = -8

    while True:
        with open("gui_input.txt", "r") as file:
            input = file.read().strip()
        if input == "finish1":
            finish = 1
            with open("gui_input.txt", "w") as file:
                pass
        else:
            if state == "WaitCall":
                if finish == 1:
                    seq_number = "Fin 1"
                    finish = 2
                elif finish == 2:
                    seq_number = "Fin 2"
                    finish = 3
                elif finish == 3:
                    break
                else:
                    seq_number += 8
                rdt_send(seq_number)
                time.sleep(6)
                state = "WaitACK"
            else:
                with open("gui_input.txt", "r") as file:
                    input = file.read()
                with open("gui_input.txt", "w") as file:
                    pass
                if input == "lost":
                    report(f"ACK {seq_number+8} timed out.")
                    rdt_send(seq_number)
                    time.sleep(6)
                    state = "WaitACK"
                elif input == "corrupt":
                    report(f"NAK {seq_number+8} received.")
                    rdt_send(seq_number)
                    time.sleep(6)
                    state = "WaitACK"
                
                else:
                    if finish and not isinstance(seq_number, int):
                        report(f"ACK {seq_number} received.")
                        state = "WaitCall"
                    else:
                        report(f"ACK {seq_number+8} received.")
                        state = "WaitCall"