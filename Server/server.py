import json
import logging
import socket
import threading

from Server.clienthandler import ClientHandler

logging.basicConfig(level=logging.INFO)

clients = set()


class AnimalShelterServer(threading.Thread):
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self)
        self.__is_connected = False
        self.host = host
        self.port = port
        # self.init_server(host, port)                #server niet onmiddellijk initialiseren (via GUI)
        self.messages_queue = messages_queue

    @property
    def is_connected(self):
        return self.__is_connected

    def init_server(self):
        # create a socket object
        print("serversocket aangemaakt op: %s:%s" % (self.host, self.port))
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        # self.print_bericht_gui_server("SERVER STARTED")
        self.print_log_info_gui("START_SERVER")

    def close_server_socket(self):
        # self.print_bericht_gui_server("CLOSE_SERVER")
        self.print_log_info_gui("CLOSE_SERVER")
        self.__is_connected = False
        self.serversocket.close()

    def run(self):
        print('def run exectuted')
        try:
            while True:
                self.print_log_info_gui("waiting for a new client...")
                print('waiting for connection')
                (clientsocket, addr) = self.serversocket.accept()
                # self.print_bericht_gui_server("CLIENTINFO: %s" % str(addr))
                print("addr = %s" % str(addr))
                print("clientsocket = %s" % clientsocket)
                self.print_user_info_gui(addr)
                clh = ClientHandler(clientsocket, self.messages_queue, addr)
                clh.start()
                clients.add(clh)
                # self.print_bericht_gui_server("Current Thread count: %i." % threading.active_count())
                self.print_log_info_gui("Current Thread count: %i." % threading.active_count())

        except Exception as ex:
            # self.print_bericht_gui_server("Serversocket afgesloten")
            print(ex)
            logging.error("Foutmelding: %s" % ex)
            self.print_log_info_gui("Serversocket afgesloten")

    def send_alert(self):
        print("I'm inside the server.py sending alerts")
        for clh in clients:
            if clh.is_connected == True:
                clh.send_alert()

    def print_user_info_gui(self, info):
        print(info)
        print("user connected")
        message = {"type": "userdata", "data": info}
        self.messages_queue.put("%s" % message)

    def print_log_info_gui(self, logmessage):
        message = {"type": "logdata", "data": logmessage}
        self.messages_queue.put("%s" % message)

    def stop_gui(self):
        message = {"type": "stop_message", "data": ""}
        self.messages_queue.put("%s" % message)

    # def print_bericht_gui_server(self, message):
    #     if "CLIENTINFO" in message:
    #         self.messages_queue.put("%s" % message)
    #     else:
    #         self.messages_queue.put("Server:> %s" % message)
