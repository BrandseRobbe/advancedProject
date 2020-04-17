import threading
import jsonpickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json


class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue, addr, user_storage):
        threading.Thread.__init__(self)
        self.is_connected = True
        self.socketclient = socketclient  # connectie with client
        self.address = addr
        self.messages_queue = messages_queue  # message queue -> link to gui server
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1

        self.user_storage = user_storage

        self.run()

    def run(self):
        # server.print_log_info_gui("User has logged in")
        message = {"type": "logdata", "data": "User has logged in"}
        self.messages_queue.put("%s" % message)
        print("user just logged in, waiting for commands")

        commando = self.in_out_clh.readline().rstrip('\n')
        loop = True
        while loop:
            jsonstring = self.in_out_clh.readline().rstrip('\n')
            messageobj = json.loads(jsonstring)
            messagetype = messageobj["type"]
            messagevalue = messageobj["value"]
            print("type: %s" % messagetype)
            print("value: %s" % messagevalue)
            print('received %s' % commando)

            if messagetype == "OUTCOMETYPE":
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

            elif messagetype == "SEXUPONOUTCOME":
                df = pd.read_csv("data/train.csv")
                outcometypes = df[['SexuponOutcome']]
                list = []
                for index, row in outcometypes.iterrows():
                    object = {"SexuponOutcome": row["SexuponOutcome"]}
                    list.append(object)
                jsonSexuponOutcome = json.dumps(list)
                self.in_out_clh.write(jsonpickle.encode(jsonSexuponOutcome) + "\n")
                self.in_out_clh.flush()
                message = {"type": "logdata", "data": "Sending SexuponOutcome back"}
                self.messages_queue.put("%s" % message)
            elif messagetype == "AGEUPONOUTCOME":
                df = pd.read_csv("data/train.csv")
                outcometypes = df[['AgeuponOutcome']]
                list = []
                for index, row in outcometypes.iterrows():
                    object = {"AgeuponOutcome": row["AgeuponOutcome"]}
                    list.append(object)
                jsonAgeuponOutcome = json.dumps(list)
                self.in_out_clh.write(jsonpickle.encode(jsonAgeuponOutcome) + "\n")
                self.in_out_clh.flush()
                message = {"type": "logdata", "data": "Sending AgeuponOutcome back"}
                self.messages_queue.put("%s" % message)

            elif messagetype == "REGISTER_ATTEMPT":
                try:
                    self.user_storage.updateFile(messagevalue)
                    response = {"type": "REGISTER_RESPONSE", "value": True}
                    self.in_out_clh.write("%s \n" % json.dumps(response))
                    self.in_out_clh.flush()
                    print("register succesfull")
                except Exception as exc:
                    print(exc)
                    response = {"type": "REGISTER_RESPONSE", "value": False}
                    self.in_out_clh.write("%s \n" % json.dumps(response))
                    self.in_out_clh.flush()
                    print("register not succesfull")

            elif messagetype == "LOGIN":
                allusers = self.user_storage.fileData
                userdata = self.in_out_clh.readline().rstrip('\n')
                validuser = False
                for user in allusers:
                    if user.email == userdata.email and user.password == userdata.email:
                        validuser = True
                        break
                object = {"loginresonse": validuser}
                self.in_out_clh.write(jsonpickle.encode(object) + "\n")
                self.in_out_clh.flush()

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
