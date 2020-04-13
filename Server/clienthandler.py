import threading
import pickle
import jsonpickle


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
            print(commando)
            if commando == "SOM":
                json_data = self.in_out_clh.readline().rstrip('\n')
                s1 = jsonpickle.decode(json_data)
                s1.som = s1.getal1 + s1.getal2
                self.in_out_clh.write(jsonpickle.encode(s1) +"\n")
                self.in_out_clh.flush()
                self.print_bericht_gui_server("Sending sum %d back" % s1)
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
