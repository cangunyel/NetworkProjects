import subprocess
import threading
import time

#no loss
#no corrupt

def clear_buffer():
    with open("gui_file.txt", 'w') as file:
        pass
    with open("senderbuffer.txt", 'w') as file:
        pass
    with open("recieverbuffer.txt", 'w') as file:
        pass
    with open("gui_figure.txt", 'w') as file:
        pass
    with open("gui_input.txt", 'w') as file:
        pass

def run_sender():
    subprocess.run(["python", "rdt1/rdt1_sender.py"])

def run_receiver():
    subprocess.run(["python", "rdt1/rdt1_reciever.py"])
def run_rdt1():
    subprocess.run(["python", "rdt1/rdt1.py"])


def main():
    # Start sender and receiver in separate threads
    clear_buffer()
    rdt_thread = threading.Thread(target=run_rdt1)
    sender_thread = threading.Thread(target=run_sender)
    receiver_thread = threading.Thread(target=run_receiver)

    rdt_thread.start()
    time.sleep(3)
    sender_thread.start()
    time.sleep(3)
    receiver_thread.start()


if __name__ == "__main__":
    main()
