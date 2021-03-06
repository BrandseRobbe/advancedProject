# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import ast
import json
import socket
from queue import Queue
from threading import Thread
from tkinter import *
import pandas as pd
import jsonpickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from matplotlib.figure import Figure

from server import AnimalShelterServer

import matplotlib

matplotlib.use('Agg')


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
        self.gegevens_text.set("Get data from user")
        self.mostsearched_text = StringVar()
        self.mostsearched_text.set("View most searched searches")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=self.start_stop_server)
        self.gegevens = Button(self, textvariable=self.gegevens_text, command=self.getUserData)
        self.mostsearched = Button(self, textvariable=self.mostsearched_text, command=self.getmostsearched)
        self.sendalert = Button(self, textvariable=self.alert_text, command=self.send_alert)
        self.sendalert.grid(row=4, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.mostsearched.grid(row=4, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        self.gegevens.grid(row=3, column=1, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
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
        del self.messages_queue

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

    def getmostsearched(self):
        print("Getting most searched")
        # t = Thread(target=self.getmostsearchedwindow)
        # t.start()
        self.getmostsearchedwindow()

    def getUserData(self):
        selected = self.lstClients.get(ACTIVE)

        if selected != "":
            client = None
            for user in self.loggedInUsers:
                if user.name == selected:
                    client = user
                    break
            if client is not None:
                # t = Thread(target=self.show_userdata, kwargs=dict(user=client))
                # t.start()
                self.show_userdata(client)

    def deleteuserwindow(self):
        self.rootuserdata.destroy()

    def show_userdata(self, user):
        # self.server.send_alert()
        self.rootuserdata = Tk()
        self.rootuserdata.geometry("350x500")
        gui_server = UserData(user, self.rootuserdata)
        # self.rootuserdata.protocol("WM_DELETE_WINDOW", self.deletesearcwindow)
        self.rootuserdata.mainloop()

    def deletesearcwindow(self):
        self.rootsearch.destroy()

    def getmostsearchedwindow(self):
        self.rootsearch = Tk()
        self.rootsearch.geometry("1900x1080")
        gui_server = getmostsearchedWindow(self.server.getmostsearched, self.rootsearch)
        # self.rootsearch.protocol("WM_DELETE_WINDOW", self.deletesearcwindow)
        self.rootsearch.state("zoomed")
        self.rootsearch.bind("<F11>", lambda event: self.rootsearch.attributes("-fullscreen", not self.rootsearch.attributes("-fullscreen")))
        self.rootsearch.bind("<Escape>", lambda event: self.rootsearch.attributes("-fullscreen", False))
        self.rootsearch.mainloop()

    def start_stop_server(self):
        print("serverstatus: %s" % self.server.is_connected)
        if self.server.is_connected:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()
            self.btn_text.set("Stop server")


class getmostsearchedWindow(Frame):
    def __init__(self, callback, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.callback = callback
        self.getMostSearchedBreed()
        self.getMostSearchedAge()
        self.getMostSearchedColor()
        self.getMostSearchedName()

    def init_window(self):
        self.master.title("Get most searched")
        self.pack(fill=BOTH, expand=1)

    def getMostSearchedBreed(self):
        dataset = pd.read_csv("searches.csv")
        results = dataset[dataset['messagetype'] == "ANIMALBREED"]
        mostsearched = results["messagevalue"].value_counts()[:5].index.tolist()
        results = results[results['messagevalue'].isin(mostsearched)]

        figureBreed = plt.figure(figsize=(6, 6))
        plt.title("Get Most Searched Breed")
        plt.hist(results["messagevalue"])
        plt.xticks(rotation=10)

        # figureOutcome.autofmt_xdate(rotation=90)
        plt.gcf().canvas.draw()
        histogram = FigureCanvasTkAgg(figureBreed, self)
        histogram.get_tk_widget().place(relx=0.05, rely=0.05, relheight=0.5, relwidth=0.40)

    def getMostSearchedAge(self):
        dataset = pd.read_csv("searches.csv")
        results = dataset[dataset['messagetype'] == "ANIMALAGE"]
        mostsearched = results["messagevalue"].value_counts()[:5].index.tolist()
        results = results[results['messagevalue'].isin(mostsearched)]

        figureAge = plt.figure(figsize=(6, 6))
        plt.title("Get Most Searched Age")
        plt.hist(results["messagevalue"])
        # figureOutcome.autofmt_xdate(rotation=90)
        plt.gcf().canvas.draw()
        histogram = FigureCanvasTkAgg(figureAge, self)
        histogram.get_tk_widget().place(relx=0.55, rely=0.05, relheight=0.40, relwidth=0.40)

    def getMostSearchedColor(self):
        dataset = pd.read_csv("searches.csv")
        results = dataset[dataset['messagetype'] == "ANIMALCOLOR"]
        mostsearched = results["messagevalue"].value_counts()[:5].index.tolist()
        results = results[results['messagevalue'].isin(mostsearched)]

        figureColor = plt.figure(figsize=(6, 6))
        plt.title("Get Most Searched Color")
        plt.hist(results["messagevalue"])
        # figureOutcome.autofmt_xdate(rotation=90)
        plt.gcf().canvas.draw()
        histogram = FigureCanvasTkAgg(figureColor, self)
        histogram.get_tk_widget().place(relx=0.05, rely=0.55, relheight=0.40, relwidth=0.40)

    def getMostSearchedName(self):
        dataset = pd.read_csv("searches.csv")
        results = dataset[dataset['messagetype'] == "ANIMALNAME"]
        mostsearched = results["messagevalue"].value_counts()[:5].index.tolist()
        results = results[results['messagevalue'].isin(mostsearched)]

        figureName = plt.figure(figsize=(6, 6))
        plt.title("Get Most Searched Name")
        plt.hist(results["messagevalue"])
        # figureOutcome.autofmt_xdate(rotation=90)
        plt.gcf().canvas.draw()
        histogram = FigureCanvasTkAgg(figureName, self)
        histogram.get_tk_widget().place(relx=0.55, rely=0.55, relheight=0.40, relwidth=0.40)


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
        Button(self, text="Send to all online users", command=lambda: self.sendAlert()).grid(row=2, column=0, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

    def sendAlert(self):
        self.callback(self.alertInput.get())
        self.master.destroy()


class UserData(Frame):
    def __init__(self, user, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.user = user
        self.init_window()

    def init_window(self):
        self.master.title(self.user.name)
        self.pack(fill=BOTH, expand=1)
        dataset = pd.read_csv("searches.csv")

        df = dataset[dataset['username'] == self.user.name]
        print(df)

        Label(self, text="Name: %s" % self.user.name, anchor=W, justify=LEFT).place(relx=0.05, rely=0.05, relwidth=0.60, relheight=0.07)
        Label(self, text="Nickname: %s" % self.user.nickname, anchor=W, justify=LEFT).place(relx=0.05, rely=0.10, relwidth=0.60, relheight=0.07)
        Label(self, text="Email: %s" % self.user.email, anchor=W, justify=LEFT).place(relx=0.05, rely=0.15, relwidth=0.60, relheight=0.07)
        Label(self, text="Search history:", anchor=W, justify=LEFT).place(relx=0.05, rely=0.25, relwidth=0.60, relheight=0.07)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.history = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.history.place(relx=0.05, rely=0.30, relwidth=0.90, relheight=0.75)

        max_len = [int(df[col].str.len().max()) for col in df.columns]
        print(max_len)
        for row in df.values.tolist():
            rowstring = ""
            for cel in row:
                rowstring += cel + " " * (max_len[row.index(cel)] - len(cel)) + " | "
            print(rowstring[:-2])
            self.history.insert(END, rowstring[:-2])
