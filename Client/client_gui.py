import logging
import socket
from tkinter import *
from tkinter import messagebox
import jsonpickle
import matplotlib.pyplot as plt


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.makeConnectionWithServer()

    def init_window(self):
        self.master.title("AnimalShelter")
        self.pack(fill=BOTH, expand=1)

        self.buttonCalculate = Button(self, text="Get outcome", command=self.GetOutcome)
        self.buttonCalculate.grid(row=4, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def __del__(self):
        self.close_connection()

    def makeConnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostbyname(socket.gethostname())
            print("hosting on %s" % host)
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.in_out_server = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            print('connection error')
            logging.error("Foutmelding: %s" % ex)

    def GetOutcome(self):
        try:
            print("sending ...")
            self.in_out_server.write("OUTCOMETYPE\n")
            self.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.in_out_server.readline().rstrip('\n')
            outcome = jsonpickle.decode(answer)
            print(type(outcome))
            print(outcome)

            # plt.show()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.in_out_server.write("%s\n" % "CLOSE")
            self.in_out_server.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")


logging.basicConfig(level=logging.INFO)
root = Tk()
# root.geometry("400x300")
app = Window(root)
root.mainloop()
