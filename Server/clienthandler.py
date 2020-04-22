import threading
import jsonpickle
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

    # called on .start()
    def run(self):
        print("user just connected, waiting for commands")
        loop = True
        while loop:
            # ontvangt van client gui
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

    def sendMessageToClient(self, messageType, messageValue):
        message = {"type": messageType, "value": messageValue}
        self.in_out_clh.write("%s \n" % json.dumps(message))
        self.in_out_clh.flush()

    def get_outcometype(self):
        df = pd.read_csv("data/train.csv")
        outcometypes = df[['OutcomeType']].values.tolist()
        outcometypes = [item[0] for item in outcometypes]
        self.sendMessageToClient("OUTCOMETYPE", outcometypes)

        message = {"type": "logdata", "data": "Sending outcometype back"}
        self.messages_queue.put("%s" % message)

    def get_breed_dropdown(self):
        df = pd.read_csv("data/train.csv")
        breed = df[['Breed']].values.tolist()
        breed = [item[0] for item in breed]
        breed = list(dict.fromkeys(breed))
        self.sendMessageToClient("BREEDDROPDOWN", breed)
        message = {"type": "logdata", "data": "Sending breed back"}
        self.messages_queue.put("%s" % message)

    def get_color_dropdown(self):
        df = pd.read_csv("data/train.csv")
        color = df[['Color']].values.tolist()
        color = [item[0] for item in color]
        color = list(dict.fromkeys(color))
        self.sendMessageToClient("COLORDROPDOWN", color)
        message = {"type": "logdata", "data": "Sending color back"}
        self.messages_queue.put("%s" % message)

    def get_age_dropdown(self):
        df = pd.read_csv("data/train.csv")
        age = df[['AgeuponOutcome']].values.tolist()
        age = [item[0] for item in age]
        age = list(dict.fromkeys(age))
        self.sendMessageToClient("AGEDROPDOWN", age)
        message = {"type": "logdata", "data": "Sending age back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_name(self, search):
        df = pd.read_csv("data/train.csv")
        search = search.lower().capitalize()
        names = df['Name']
        if search in names.values.tolist():
            print("De naam zit in de dataset")
            animal_name = df[["Breed", "AgeuponOutcome", "Color"]].loc[df['Name'] == search]
            jsonBreed = json.dumps(animal_name.values.tolist())
            self.sendMessageToClient("ANIMALNAME", jsonBreed)
        else:
            print("De naam zit niet in de dataset")
            animal_name = "No animals found"
            self.sendMessageToClient("ANIMALNAME", animal_name)

        message = {"type": "logdata", "data": "Sending animals by name back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_breed(self, search):
        df = pd.read_csv("data/train.csv")
        animal_breed = df[["Name", "AgeuponOutcome", "Color"]].loc[df['Breed'] == search]
        jsonBreed = json.dumps(animal_breed.values.tolist())
        self.sendMessageToClient("ANIMALBREED", jsonBreed)
        message = {"type": "logdata", "data": "Sending animals by breed back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_color(self, search):
        df = pd.read_csv("data/train.csv")
        animal_color = df[["AgeuponOutcome", "Breed"]].loc[df['Color'] == search]
        jsonColor = json.dumps(animal_color.values.tolist())
        self.sendMessageToClient("ANIMALCOLOR", jsonColor)
        message = {"type": "logdata", "data": "Sending animals by color back"}
        self.messages_queue.put("%s" % message)

    def get_animal_by_age(self, search):
        df = pd.read_csv("data/train.csv")
        animal_age = df[["Color", "Breed"]].loc[df['AgeuponOutcome'] == search]
        jsonAge = json.dumps(animal_age.values.tolist())
        print(jsonAge)
        self.sendMessageToClient("ANIMALAGE", jsonAge)
        message = {"type": "logdata", "data": "Sending animals by age back"}
        self.messages_queue.put("%s" % message)

    def register_client(self, messagevalue):
        try:
            #first check if email already in use
            userobj = jsonpickle.decode(messagevalue)
            exists = False
            for user in self.user_storage.fileData:
                user = jsonpickle.decode(user)
                if user.email == userobj.email:
                    exists = True
                    break
            if not exists:
                # update storage
                self.user_storage.updateFile(messagevalue)
                self.sendMessageToClient("REGISTER_RESPONSE", True)
                print("register succesfull")
                self.client = jsonpickle.decode(messagevalue)
                self.show_client_servergui()
            else:
                self.sendMessageToClient("REGISTER_RESPONSE", False)
                print("email already in use")
        except Exception as exc:
            print(exc)
            self.sendMessageToClient("REGISTER_RESPONSE", False)
            print("register not succesfull")

    def login_client(self, messagevalue):
        allusers = self.user_storage.fileData
        client = jsonpickle.decode(messagevalue)
        validuser = False
        for user in allusers:
            user = jsonpickle.decode(user)
            if user.email == client.email and user.password == client.password:
                validuser = True
                print('login succesfull')
                self.client = user
                self.show_client_servergui()
                break
        self.sendMessageToClient("LOGIN_RESPONSE", validuser)
        print("login: %s" % validuser)

    def show_client_servergui(self):
        message = {"type": "logdata", "data": "User has logged in"}
        self.messages_queue.put("%s" % message)
        message = {"type": "userdata", "data": self.client.name}
        self.messages_queue.put("%s" % message)

    def send_alert(self, alertmessage):
        print("SENDING ALERT %s" % alertmessage)
        self.sendMessageToClient("ALERT", alertmessage)
        logmessage = {"type": "logdata", "data": "Sending alert %s" % alertmessage}
        self.messages_queue.put("%s" % logmessage)

    # def print_bericht_gui_server(self, message):
    #     if "CLIENTINFO: CONNECTION CLOSED: " in message:
    #         self.messages_queue.put("%s" % (message))
    #     else:
    #         self.messages_queue.put("CLH %d:> %s" % (self.id, message))
