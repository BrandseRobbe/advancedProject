import logging
import socket
from tkinter import *
from tkinter import messagebox
import jsonpickle
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
        self.buttonCalculate.place(relx = 0.05, rely = 0.05, relheight= 0.05, relwidth = 0.1875)
        self.buttonCalculate = Button(self, text="Get Sex", command=self.GetSexuponOutcome)
        self.buttonCalculate.place(relx = 0.2875, rely = 0.05, relheight= 0.05, relwidth = 0.1875)
        self.buttonCalculate = Button(self, text="Get Age", command=self.GetAgeuponOutcome)
        self.buttonCalculate.place(relx=0.525, rely=0.05, relheight=0.05, relwidth=0.1875)
        self.buttonCalculate = Button(self, text="Get ...", command=self.GetAgeuponOutcome)
        self.buttonCalculate.place(relx= 0.7625, rely=0.05, relheight=0.05, relwidth=0.1875)





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

    def ProcessData(self, input, order):
        breed = json.loads(input)
        breed = jsonpickle.decode(breed)
        outcomeList = []
        for item in breed:
            outcomeList.append(item[order])

        return outcomeList

    def GetOutcome(self):
        try:
            print("sending ...")
            self.in_out_server.write("OUTCOMETYPE\n")
            self.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.in_out_server.readline().rstrip('\n')
            outcomeList = self.ProcessData(answer, "OutcomeType")
            f = Figure(figsize=(6, 6), dpi=100)
            canvas = FigureCanvasTkAgg(f, self)
            canvas.get_tk_widget().place(relx = 0.03, rely = 0.15, relheight=0.80, relwidth = 0.2275 )
            p = f.gca()
            p.hist(outcomeList)
            canvas.draw()
            print("Done!")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def GetSexuponOutcome(self):
        try:
            print("sending ...")
            self.in_out_server.write("SEXUPONOUTCOME\n")
            self.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.in_out_server.readline().rstrip('\n')
            SexuponOutcomeList = self.ProcessData(answer, "SexuponOutcome")

            f = Figure(figsize=(6, 6), dpi=100)
            canvas = FigureCanvasTkAgg(f, self)
            canvas.get_tk_widget().place(relx = 0.2675, rely = 0.15, relheight= 0.80, relwidth = 0.2275)
            p = f.gca()
            p.hist(SexuponOutcomeList)
            canvas.draw()
            print("Done!")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def GetAgeuponOutcome(self):
        try:
            print("sending ...")
            self.in_out_server.write("AGEUPONOUTCOME\n")
            self.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.in_out_server.readline().rstrip('\n')
            AgeuponOutcomeList = self.ProcessData(answer, "AgeuponOutcome")
            f = Figure(figsize=(6, 6), dpi=100)
            canvas = FigureCanvasTkAgg(f, self)
            canvas.get_tk_widget().place(relx=0.505, rely=0.15, relheight=0.80, relwidth=0.2275)
            p = f.gca()
            p.hist(AgeuponOutcomeList)
            plt.xticks(rotation='vertical')
            canvas.draw()
            print("Done!")

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
root.geometry("1900x1080")
app = Window(root)
root.mainloop()
