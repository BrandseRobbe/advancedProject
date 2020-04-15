import threading
import pickle
import jsonpickle
import seaborn as sns
import pandas as pd

from Server import server


class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue, addr):
        threading.Thread.__init__(self)
        self.is_connected = True
        self.socketclient = socketclient # connectie with client
        self.address = addr
        self.messages_queue = messages_queue #message queue -> link to gui server
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1

        self.run()

    def run(self):
        # server.print_log_info_gui("User has logged in")
        message = {"type": "logdata", "data": "User has logged in"}
        self.messages_queue.put("%s" % message)

        print("user just logged in, waiting for commands")
        commando = self.in_out_clh.readline().rstrip('\n')
        print(commando)
        while commando != "CLOSE":
            print('commando clienthandler: %s' % commando)
            if commando == "OUTCOMETYPE":
                df = pd.read_csv("../data/test.csv", skiprows=1)
                OutcomeTypeVar = sns.countplot(x="OutcomeType", data=df)
                print(OutcomeTypeVar)
                self.in_out_clh.write(jsonpickle.encode(OutcomeTypeVar) + "\n")
                print(jsonpickle.encode(OutcomeTypeVar))
                self.in_out_clh.flush()
                self.print_bericht_gui_server("Sending sum %d back" % OutcomeTypeVar)

            commando = self.in_out_clh.readline().rstrip('\n')

        self.print_bericht_gui_server("CLIENTINFO: CONNECTION CLOSED: %s" % str(self.address))
        self.is_connected = False
        self.socketclient.close()

    def send_alert(self):
        print("SENDING ALERT")
        bericht = "ALERT"
        self.in_out_clh.write(jsonpickle.encode(bericht) + "\n")
        self.in_out_clh.flush()
        self.print_bericht_gui_server("Sending alert %s" % bericht)

    def print_bericht_gui_server(self, message):
        if "CLIENTINFO: CONNECTION CLOSED: " in message:
            self.messages_queue.put("%s" % (message))
        else:
            self.messages_queue.put("CLH %d:> %s" % (self.id, message))
