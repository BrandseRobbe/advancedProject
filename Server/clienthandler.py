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
        self.client = None
        self.run()

    def run(self):
        print("user just connected, waiting for commands")
        loop = True
        while loop:
            jsonstring = self.in_out_clh.readline().rstrip('\n')
            messageobj = json.loads(jsonstring)
            messagetype = messageobj["type"]
            messagevalue = messageobj["value"]
            print("type: %s" % messagetype)
            print("value: %s" % messagevalue)

            if messagetype == "OUTCOMETYPE":
                self.get_outcometype()

            elif messagetype == "BREEDDROPDOWN":
                self.get_breed_dropdown()

            elif messagetype == "COLORDROPDOWN":
                self.get_color_dropdown()

            elif messagetype == "AGEDROPDOWN":
                self.get_age_dropdown()

            elif messagetype == "ANIMALBREED":
                self.get_animal_by_breed(messagevalue)

            elif messagetype == "ANIMALCOLOR":
                self.get_animal_by_color(messagevalue)

            elif messagetype == "ANIMALAGE":
                self.get_animal_by_age(messagevalue)

            elif messagetype == "ANIMALNAME":
                self.get_animal_by_name(messagevalue)

            elif messagetype == "REGISTER_ATTEMPT":
                self.register_client(messagevalue)

            elif messagetype == "LOGIN_ATTEMPT":
                self.login_client(messagevalue)

        message = {"type": "logdata", "data": "Connection closed: %s" % str(self.address)}
        self.messages_queue.put("%s" % message)
        self.is_connected = False
        self.socketclient.close()

    def get_outcometype(self):
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

    def get_breed_dropdown(self):
        df = pd.read_csv("data/train.csv")
        breed = df[['Breed']]
        list = []
        for index, row in breed.iterrows():
            object = {"Breed": row["Breed"]}
            list.append(object)
        jsonBreed = json.dumps(list)
        self.in_out_clh.write(jsonpickle.encode(jsonBreed) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending breed back"}
        self.messages_queue.put("%s" % message)

    def get_color_dropdown(self):
        df = pd.read_csv("data/train.csv")
        color = df[['Color']]
        list = []
        for index, row in color.iterrows():
            object = {"Color": row["Color"]}
            list.append(object)
        jsonColor = json.dumps(list)
        self.in_out_clh.write(jsonpickle.encode(jsonColor) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending color back"}
        self.messages_queue.put("%s" % message)

    def get_age_dropdown(self):
        df = pd.read_csv("data/train.csv")
        age = df[['Age']]
        list = []
        for index, row in age.iterrows():
            object = {"Age": row["Age"]}
            list.append(object)
        jsonAge = json.dumps(list)
        self.in_out_clh.write(jsonpickle.encode(jsonAge) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending age back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_name(self, search):
        df = pd.read_csv("data/train.csv")
        animal_name = df.loc[df['Name'] == search]
        jsonName = json.dumps(animal_name)
        self.in_out_clh.write(jsonpickle.encode(jsonName) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending animals by name back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_breed(self, search):
        df = pd.read_csv("data/train.csv")
        animal_breed = df.loc[df['Breed'] == search]
        jsonBreed = json.dumps(animal_breed)
        self.in_out_clh.write(jsonpickle.encode(jsonBreed) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending animals by breed back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_color(self, search):
        df = pd.read_csv("data/train.csv")
        animal_color = df.loc[df['Color'] == search]
        jsonColor = json.dumps(animal_color)
        self.in_out_clh.write(jsonpickle.encode(jsonColor) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending animals by color back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_age(self, search):
        df = pd.read_csv("data/train.csv")
        animal_age = df.loc[df['Age'] == search]
        jsonAge = json.dumps(animal_age)
        self.in_out_clh.write(jsonpickle.encode(jsonAge) + "\n")
        self.in_out_clh.flush()
        message = {"type": "logdata", "data": "Sending animals by age back"}
        self.messages_queue.put("%s" % message)

    def register_client(self, messagevalue):
        try:
            self.user_storage.updateFile(messagevalue)
            response = {"type": "REGISTER_RESPONSE", "value": True}
            self.in_out_clh.write("%s \n" % json.dumps(response))
            self.in_out_clh.flush()
            print("register succesfull")
            self.client = jsonpickle.decode(messagevalue)
            self.show_client_servergui()
        except Exception as exc:
            print(exc)
            response = {"type": "REGISTER_RESPONSE", "value": False}
            self.in_out_clh.write("%s \n" % json.dumps(response))
            self.in_out_clh.flush()
            print("register not succesfull")

    def login_client(self, messagevalue):
        allusers = self.user_storage.fileData
        client = jsonpickle.decode(messagevalue)
        validuser = False
        for user in allusers:
            print(user)
            user = jsonpickle.decode(user)
            print("%s == %s and %s == %s" % (user.email, client.email, user.password, client.password))
            if user.email == client.email and user.password == client.password:
                validuser = True
                print('login succesufull')
                self.client = user
                self.show_client_servergui()
                break
        response = {"type": "LOGIN_RESPONSE", "value": validuser}
        self.in_out_clh.write("%s \n" % json.dumps(response))
        self.in_out_clh.flush()
        print("login: %s" % validuser)

    def show_client_servergui(self):
        message = {"type": "logdata", "data": "User has logged in"}
        self.messages_queue.put("%s" % message)
        message = {"type": "userdata", "data": self.client.name}
        self.messages_queue.put("%s" % message)

    def send_alert(self, alertmessage):
        print("SENDING ALERT")
        alertmessage = {"type": "ALERT", "data":alertmessage}
        self.in_out_clh.write(json.dumps(alertmessage) + "\n")
        self.in_out_clh.flush()
        logmessage = {"type": "logdata", "data": "Sending alert %s" % bericht}
        self.messages_queue.put("%s" % logmessage)

    # def print_bericht_gui_server(self, message):
    #     if "CLIENTINFO: CONNECTION CLOSED: " in message:
    #         self.messages_queue.put("%s" % (message))
    #     else:
    #         self.messages_queue.put("CLH %d:> %s" % (self.id, message))
