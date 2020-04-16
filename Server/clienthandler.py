import threading
import jsonpickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json

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
                df = pd.read_csv("data/train.csv")
                outcometypes = df[['OutcomeType']]
                list = []
                for index, row in outcometypes.iterrows():
                    object = {"OutcomeType": row["OutcomeType"]}
                    list.append(object)
                jsonOutcomeTypes = json.dumps(list)
                self.in_out_clh.write(jsonpickle.encode(jsonOutcomeTypes) + "\n")
                self.in_out_clh.flush()
                message = {"type": "logdata", "data": "Sending outcometype back"}
                self.messages_queue.put("%s" % message)

            commando = self.in_out_clh.readline().rstrip('\n')

        message = {"type": "logdata", "data": "Connection closed: %s" % str(self.address)}
        self.messages_queue.put("%s" % message)
        self.is_connected = False
        self.socketclient.close()

    def send_alert(self):
        print("SENDING ALERT")
        bericht = "ALERT"
        self.in_out_clh.write(jsonpickle.encode(bericht) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending alert %s" % bericht}
        self.messages_queue.put("%s" % message)

    # def print_bericht_gui_server(self, message):
    #     if "CLIENTINFO: CONNECTION CLOSED: " in message:
    #         self.messages_queue.put("%s" % (message))
    #     else:
    #         self.messages_queue.put("CLH %d:> %s" % (self.id, message))
