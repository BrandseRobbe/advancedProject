import logging
import socket
import threading

from PickleRepo import PickleRepo
from clienthandler import ClientHandler

logging.basicConfig(level=logging.INFO)



class AnimalShelterServer(threading.Thread):
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self)
        self.__is_connected = False
        self.host = host
        self.port = port
        self.messages_queue = messages_queue
        self.user_storage = PickleRepo()
        self.clients = set()

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
        self.print_log_info_gui("START_SERVER")

    def close_server_socket(self):
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
                self.user_storage = PickleRepo()
                clh = ClientHandler(clientsocket, self.messages_queue, addr, self.user_storage)
                clh.start()
                self.clients.add(clh)
                self.print_log_info_gui("Current Thread count: %i." % threading.active_count())

        except Exception as ex:
            print(ex)
            logging.error("Foutmelding: %s" % ex)
            self.print_log_info_gui("Serversocket afgesloten")

    def send_alert(self, alertmessage):
        print("I'm inside the server.py sending alerts")
        for clh in self.clients:
            if clh.is_connected == True:
                clh.send_alert(alertmessage)

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
