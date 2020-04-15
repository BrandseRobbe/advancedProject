import threading
import pickle
import jsonpickle
import seaborn as sns
import pandas as pd

class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue, addr):
        threading.Thread.__init__(self)
        self.is_connected = True
        # connectie with client
        self.socketclient = socketclient
        self.address = addr
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1



    def run(self):
        self.print_bericht_gui_server("User has logged in")
        commando = self.in_out_clh.readline().rstrip('\n')
        while (commando != "CLOSE"):
            if commando == "OUTCOMETYPE":
                self.messages_queue.put("LOG:> We made it")
                df = pd.read_csv("./data/test.csv", skiprows=1)
                OutcomeTypeVar = sns.countplot(x="OutcomeType", data=df)
                print(OutcomeTypeVar)
                self.in_out_clh.write(jsonpickle.encode(OutcomeTypeVar) +"\n")
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
