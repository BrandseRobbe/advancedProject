# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *

from Server.server import AnimalShelterServer


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_messages_queue()
        self.init_server()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        Label(self, text="Log-berichten:").grid(row=0)
        Label(self, text="Online Users:").grid(row=0, column=1)
        self.lstClients = Listbox(self, width= 35)
        #self.lstClients.config(command=self.lstClients.yview)
        self.lstClients.grid(row=1, column=1, sticky=N + S + E + W)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)
        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=0, sticky=N + S)
        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.alert_text = StringVar()
        self.alert_text.set("Send alert to all online users")
        self.gegevens_text = StringVar()
        self.gegevens_text.set("Get data from all users")
        self.mostsearched_text = StringVar()
        self.mostsearched_text.set("View most searched searches")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=self.start_stop_server)
        self.gegevens = Button(self, textvariable=self.gegevens_text)
        self.mostsearched = Button(self, textvariable=self.mostsearched_text)
        self.sendalert = Button(self, textvariable=self.alert_text, command=self.send_alert)
        self.gegevens.grid(row=4, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.mostsearched.grid(row=4, column=0,  pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.sendalert.grid(row=3, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.buttonServer.grid(row=3, column=0,  pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def init_server(self):
        # server - init
        self.server = AnimalShelterServer(socket.gethostname(), 9999, self.messages_queue)


    def afsluiten_server(self):
        if self.server != None:
            self.server.close_server_socket()
        # del (self.messages_queue)

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while message != "CLOSE_SERVER":
            if "CLIENTINFO" in message:
                if "CONNECTION CLOSED" in message:
                    delmessage = message.replace("CLIENTINFO: CONNECTION CLOSED: ", "")
                    label = "Zarin"
                    idx = self.lstClients.get(0, END).index(label)
                    self.lstClients.delete(idx)
                    self.lstClients.delete(0, END)
                    message = self.messages_queue.get()
                set = message.replace("CLIENTINFO:", "")
                self.lstClients.insert(END, "Zarin")
                self.messages_queue.task_done()
                message = self.messages_queue.get()
            else:
                self.lstnumbers.insert(END, message)
                self.messages_queue.task_done()
                message = self.messages_queue.get()
        print("queue stop")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue)
        t.start()

    def send_alert(self):
        print("Sending alerts to clients")
        self.server.send_alert()


    def start_stop_server(self):
        print(self.server.is_connected)
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()             #thread!
            self.btn_text.set("Stop server")

