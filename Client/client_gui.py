# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from tkinter import *
from tkinter import messagebox


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.makeConnectionWithServer()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("AnimalShelter")
        # self.master.geometry("400x300")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Label(self, text="Snelheid:").grid(row=0)
        # self.entry_snelheid = Entry(self, width=40)
        # self.entry_snelheid.grid(row=0, column=1, sticky=E + W, padx=(5, 5), pady =(5,5))

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
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)

    def GetOutcome(self):
        try:
            print("test")
            self.my_writer_obj.write("OUTCOMETYPE")
            self.my_writer_obj.flush()

            # waiting for answer
            answer = self.my_writer_obj.readline().rstrip('\n')
            outcome = str(answer)
            print(outcome)

            self.label_resultaat['text'] = "{0}".format(outcome)

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("%s\n" % "CLOSE")
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")


logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = Window(root)
root.mainloop()