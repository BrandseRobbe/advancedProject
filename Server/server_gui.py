# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import ast
import json
import socket
from queue import Queue
from threading import Thread
from tkinter import *

import jsonpickle

from server import AnimalShelterServer


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_messages_queue()
        self.init_server()
        self.loggedInUsers = []

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        Label(self, text="Log-berichten:").grid(row=0)
        Label(self, text="Online Users:").grid(row=0, column=1)
        self.lstClients = Listbox(self, width=35)
        # self.lstClients.config(command=self.lstClients.yview)
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
        self.mostsearched.grid(row=4, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.sendalert.grid(row=3, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.buttonServer.grid(row=3, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def init_server(self):
        # server - init
        host = socket.gethostbyname(socket.gethostname())
        print("hosting on %s" % host)
        self.server = AnimalShelterServer(host, 9999, self.messages_queue)

    def afsluiten_server(self):
        if self.server is not None:
            self.server.close_server_socket()
        # del (self.messages_queue)

    def print_messsages_from_queue(self):
        indexlog = 0
        indexuser = 0
        loop = True

        # message = json.loads(message.replace("\'", "\""))
        while loop:
            message = self.messages_queue.get()
            print("message queue: %s" % message)
            message = ast.literal_eval(message)

            messageType = message["type"]
            messageData = message["data"]
            if messageType == "userdata":
                client = jsonpickle.decode(messageData)
                print("name: %s" % client.name)
                self.lstClients.insert(len(self.loggedInUsers), client.name)
                self.loggedInUsers.append(client)
            elif messageType == "removeUser":
                client = jsonpickle.decode(messageData)
                actualclient = None
                for user in self.loggedInUsers:
                    if user.email == client.email and user.password == client.password:
                        actualclient = user
                self.lstClients.delete(self.loggedInUsers.index(actualclient))
                self.loggedInUsers.remove(actualclient)
            elif messageType == "logdata":
                self.lstnumbers.insert(indexlog, messageData)
                indexlog += 1
            elif messageType == "stop_message":
                loop = False
        print("queue stop")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue)
        t.start()

    def send_alert(self):
        print("Sending alerts to clients")
        t = Thread(target=self.send_alert_window)
        t.start()

    def send_alert_window(self):
        # self.server.send_alert()
        root = Tk()
        # root.geometry("300x100")
        gui_server = SendNotificationWindow(self.server.send_alert, root)
        # root.protocol("WM_DELETE_WINDOW", callback)
        root.mainloop()

    def start_stop_server(self):
        print("serverstatus: %s" % self.server.is_connected)
        if self.server.is_connected:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()
            self.btn_text.set("Stop server")


class SendNotificationWindow(Frame):
    def __init__(self, callback, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.callback = callback

    def init_window(self):
        self.master.title("Alert")
        self.pack(fill=BOTH, expand=1)
        Label(self, text="Send alert to all online users: ").grid(row=0, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.alertInput = Entry(self, text="testtext")
        self.alertInput.grid(row=1, column=0)
        Button(self, text="Send all online users", command=lambda: self.sendAlert()).grid(row=2, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

    def sendAlert(self):
        self.callback(self.alertInput.get())
        self.master.destroy()
