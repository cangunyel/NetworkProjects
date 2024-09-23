import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import re
import random

# GUI class for a four-section layout
class FourSectionsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Four Sections GUI")

        # Create four frames for the sections
        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.master, bg="lightgray")
        self.frame4 = tk.Frame(self.master, bg="lightyellow")

        # Set a default size for each frame
        default_size = 200
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=0, column=1, sticky="nsew")
        self.frame3.grid(row=1, column=0, sticky="nsew")
        self.frame4.grid(row=1, column=1, sticky="nsew")

        self.frame1.grid_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame3.grid_propagate(False)
        self.frame4.grid_propagate(False)

        self.frame1["width"] = default_size
        self.frame1["height"] = default_size
        self.frame2["width"] = default_size
        self.frame2["height"] = default_size
        self.frame3["width"] = default_size
        self.frame3["height"] = default_size
        self.frame4["width"] = default_size
        self.frame4["height"] = default_size

        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        # Text widget for displaying results in the left bottom corner
        self.result_text = scrolledtext.ScrolledText(
            self.frame3, wrap=tk.WORD, width=30
        )
        self.result_text.pack(expand=True, fill=tk.BOTH)

       
        # Entry widget for user input
        self.user_input_entry = tk.Entry(self.frame4)
        self.user_input_entry.place(x=300, y=100)

        # Check Input button
        self.check_input_button = tk.Button(self.frame4, text="Check Input", command=self.check_input)
        self.check_input_button.place(x=300, y=150)

        # Text widgets for function calls
        self.text_part1 = tk.Text(self.frame4, wrap=tk.WORD, width=60, height=8)
        self.text_part1.place(x=100, y=200)
        
        self.text_part2 = tk.Text(self.frame4, wrap=tk.WORD, width=60, height=8)
        self.text_part2.place(x=100, y=350)
        
        self.text_part3 = tk.Text(self.frame4, wrap=tk.WORD, width=8, height=1)
        self.text_part3.place(x=25, y=180)
        self.text_part3.insert(tk.END, "Receiver")
        
        self.text_part4 = tk.Text(self.frame4, wrap=tk.WORD, width=8, height=1)
        self.text_part4.place(x=25, y=330)
        self.text_part4.insert(tk.END, "Sender")

        # FSM Images
        self.tk_image1 = None
        self.tk_image2 = None
        self.image_path1 = "tcp/tcpclient_closed.png"
        self.image_path2 = "tcp/tcpserver_listen.png"

        self.tk_figure1 = None
        self.figure_path1 = "figure/figure_rdtsend.png"

        self.result_text.insert(
            tk.END,
            "                                Server                                   Client"
            + "\n",
        )

        # Create a thread for image loading and displaying
        threading.Thread(target=self.update_results).start()
        threading.Thread(target=self.show_images).start()
        threading.Thread(target=self.show_figure).start()

    def show_figure(self):
        figure1 = Image.open(self.figure_path1)

        # Resize images 
        figure1 = figure1.resize((300, 300), Image.LANCZOS)
        # Convert images to Tkinter PhotoImage objects
        self.tk_figure1 = ImageTk.PhotoImage(figure1)

        canvas_width = 700
        canvas_height = 450

        # Clear existing images
        for widget in self.frame1.winfo_children():
            widget.destroy()

        # Display the images
        canvas = tk.Canvas(
            self.frame1, width=canvas_width, height=canvas_height, bg="black"
        )
        canvas.grid(row=0, column=0, sticky="nsew")

        canvas.create_image(350, 160, anchor=tk.CENTER, image=self.tk_figure1)

    def show_images(self):
        image1 = Image.open(self.image_path1)
        image2 = Image.open(self.image_path2)

        # Resize images
        image1 = image1.resize((300, 300), Image.LANCZOS)
        image2 = image2.resize((300, 300), Image.LANCZOS)

        # Convert images to Tkinter PhotoImage objects
        self.tk_image1 = ImageTk.PhotoImage(image1)
        self.tk_image2 = ImageTk.PhotoImage(image2)

        canvas_width = 700
        canvas_height = 450

        # Clear existing images
        for widget in self.frame2.winfo_children():
            widget.destroy()

        # Display the images 
        canvas = tk.Canvas(
            self.frame2, width=canvas_width, height=canvas_height, bg="black"
        )
        canvas.grid(row=0, column=0, sticky="nsew")

        canvas.create_image(520, 170, anchor=tk.CENTER, image=self.tk_image1)
        canvas.create_image(190, 170, anchor=tk.CENTER, image=self.tk_image2)

    def check_input(self):
        user_input = self.user_input_entry.get()  
        if user_input == "corrupt":
            with open("gui_input.txt", "w") as file:
                file.write("corrupt")

        elif user_input == "lost":
            with open("gui_input.txt", "w") as file:
                file.write("lost")
        elif user_input == "finish":
            with open("gui_input.txt", "w") as file:
                file.write("finish1")

    def switch_photos(self, new_path1=None, new_path2=None):
        if new_path1 is not None:
            self.image_path1 = new_path1
        if new_path2 is not None:
            self.image_path2 = new_path2

        # Redraw the images
        self.show_images()

    def switch_figure(self, new_path1):
        self.figure_path1 = new_path1
        # Redraw the images
        self.show_figure()

    def read_and_erase_from_file(self, filename):
        with open(filename, "r") as file:
            message = file.read()

        # Erase the content of the file after reading
        with open(filename, "w") as file:
            file.write("")

        return message

    def clear_text_parts(self):
        # Clear the content of all Text widgets
        self.text_part1.delete(1.0, tk.END)
        self.text_part2.delete(1.0, tk.END)
        
    def update_results(self):
        received_message = self.read_and_erase_from_file("gui_file.txt")
        figure = self.read_and_erase_from_file("gui_figure.txt")
        print("--------------")
        # figure
        print(figure)
        if re.match(r"udt_send()", figure):
            self.switch_figure("figure/figure_udtsend.png")
        elif re.match(r"rdt_send()", figure):
            self.switch_figure("figure/figure_rdtsend.png")
        elif re.match(r"rdt_rcv()", figure):
            self.switch_figure("figure/figure_rdtrcvpng.png")
        elif re.match(r"deliver_data()", figure):
            self.switch_figure("figure/figure_deliverdata.png")

        if received_message:

            if re.match(r"Packet \d+ sent\.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       -------------------------------->"
                    + "\n",
                )
            elif re.match(r"ACK \d+ timed out\.", received_message):
                if random.choice([0, 1]):
                    self.result_text.insert(
                        tk.END,
                        "                                                       X<---------------"
                        + "\n",
                    )
                else:
                    self.result_text.insert(
                        tk.END,
                        "                                       --------------->X                "
                        + "\n",
                    )
            elif re.match(r"ACK \d+ sent\.", received_message) or re.match(
                r"NAK \d+ sent\.", received_message
            ):
                self.result_text.insert(
                    tk.END,
                    "                                       <--------------------------------"
                    + "\n",
                )
            # handshake
            elif re.match(r"Handshake request with SYN=1.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       <--------------------------------"
                    + "\n",
                )
                self.switch_photos(new_path1="tcp/tcpclient_syn_sent.png")
                self.clear_text_parts()
                self.text_part1.insert(tk.END,"active OPEN\n\n"+"create TCB\nsend SYN")
            elif re.match(r"Handshake accepted with SYN=1.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       -------------------------------->"
                    + "\n",
                )
                self.switch_photos(new_path2="tcp/tcpserver_syn_rcv.png")
                self.clear_text_parts()
                self.text_part2.insert(tk.END,"rcv SYN\n\n"+"send SYN\nsend ACK")
            elif re.match(
                r"Client acknowlegded connection. Changed SYN=0.", received_message
            ):
                self.result_text.insert(
                    tk.END,
                    "                                       <--------------------------------"
                    + "\n",
                )
                self.switch_photos("tcp/tcpclient_estab.png", "tcp/tcpserver_estab.png")
                self.clear_text_parts()
                self.text_part1.insert(tk.END,"rcv SYN,ACK\n\n"+"send ACK")
                self.text_part2.insert(tk.END,"rcv ACK of SYN")
            # finish
            elif re.match(r"Packet Fin 1 sent.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       <--------------------------------"
                    + "\n",
                )
                self.switch_photos(new_path1="tcp/tcpclient_fin_wait_1.png")
                self.clear_text_parts()
                self.text_part1.insert(tk.END,"CLOSE\n\n"+"send FIN")
            elif re.match(r"Packet Fin 2 sent.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       -------------------------------->"
                    + "\n",
                )
                self.switch_photos(new_path2="tcp/tcpserver_last_ack.png")
                self.clear_text_parts()
                self.text_part2.insert(tk.END,"CLOSE\n\n"+"send FIN")
            elif re.match(r"ACK Fin 1 sent.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       -------------------------------->"
                    + "\n",
                )
                self.switch_photos(new_path2="tcp/tcpserver_close_wait.png")
                self.clear_text_parts()
                self.text_part2.insert(tk.END,"rcvFIN\n\n"+"send ACK")
            elif re.match(r"ACK Fin 2 sent.", received_message):
                self.result_text.insert(
                    tk.END,
                    "                                       <--------------------------------"
                    + "\n",
                )
                self.switch_photos(new_path1="tcp/tcpclient_time_wait.png")
                self.clear_text_parts()
                self.text_part1.insert(tk.END,"rcv FIN\n\n"+"send ACK")
            elif re.match(r"ACK Fin 1 received.", received_message):
                self.switch_photos(new_path1="tcp/tcpclient_fin_wait_2.png")
                self.clear_text_parts()
                self.text_part1.insert(tk.END,"rcv ACK of FIN")
            elif re.match(r"ACK Fin 2 received.", received_message):
                self.switch_photos(new_path2="tcp/tcpserver_closed.png")
                self.clear_text_parts()
                self.text_part2.insert(tk.END,"rcv ACK of FIN")
                self.text_part1.insert(tk.END,"Timeout=30sec\n\n"+"delete TCB  ")
                self.master.after(30000,lambda: self.switch_photos(new_path1="tcp/tcpclient_closed.png") )
            self.result_text.insert(tk.END, received_message + "\n")
            self.result_text.see(tk.END)  # Scroll to the bottom

        # Schedule the update_results method to be called after
        self.master.after(500, self.update_results)


def main():
    root = tk.Tk()
    app = FourSectionsGUI(root)
    root.state("zoomed")
    root.mainloop()


if __name__ == "__main__":
    main()
