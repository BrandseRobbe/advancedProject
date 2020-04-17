import logging
import socket
from threading import Thread
from tkinter import *
from tkinter import messagebox
import jsonpickle
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Models.User import User


class Client(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Setup frame
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)

        self.frames = {}
        pages = [Login, Register, Applicatie]

        for f in pages:
            frame = f(container, self)
            self.frames[f] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.makeConnectionWithServer()
        responseloop = Thread(target=self.getserverresponse)
        responseloop.start()
        self.showFrame(Login)

    def showFrame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()

    def makeConnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostbyname(socket.gethostname())
            print("hosting on %s" % host)
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.in_out_server = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            print('connection error')
            logging.error("Foutmelding: %s" % ex)

    def getserverresponse(self):
        print("starting response loop")
        loop = True
        while loop:
            print("waiting for message ...")
            jsonstring = self.in_out_server.readline().rstrip('\n')
            messageobj = json.loads(jsonstring)
            messagetype = messageobj["type"]
            messagevalue = messageobj["value"]

            if messagetype == "REGISTER_RESPONSE":
                self.handleRegister(messagevalue)
            elif messagetype == "LOGIN_RESPONSE":
                self.handlelogin(messagevalue)
            elif messagetype == "ALERT":
                self.handleAlert(messagevalue)

    def handleRegister(self, allowed):
        if allowed:
            # volgende frame
            pass
        else:
            # showregistererror()
            pass

    def handleLogin(self, allowed):
        if allowed:
            # volgende frame
            pass
        else:
            # showregistererror()
            pass

    def handleAlert(self, message):
        pass

    def close_connection(self):
        try:
            self.socket_to_server.close()
            logging.info("Connection closed with client")
        except Exception as ex:
            logging.error("Error: %s" % ex)

    # --- Closing window ---
    def __del__(self):
        self.in_out_server.write("CLOSE\n")
        self.in_out_server.flush()
        self.close_connection()


class Applicatie(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # controller = self van client

        self.pack(fill=BOTH, expand=1)

        self.buttonCalculate = Button(self, text="Get outcome", command=self.GetOutcome)
        self.buttonCalculate.place(relx=0.05, rely=0.05, relheight=0.05, relwidth=0.1875)
        self.buttonCalculate = Button(self, text="Get Sex", command=self.GetSexuponOutcome)
        self.buttonCalculate.place(relx=0.2875, rely=0.05, relheight=0.05, relwidth=0.1875)
        self.buttonCalculate = Button(self, text="Get Age", command=self.GetAgeuponOutcome)
        self.buttonCalculate.place(relx=0.525, rely=0.05, relheight=0.05, relwidth=0.1875)
        self.buttonCalculate = Button(self, text="Get ...", command=self.GetAgeuponOutcome)
        self.buttonCalculate.place(relx=0.7625, rely=0.05, relheight=0.05, relwidth=0.1875)

    def ProcessData(self, input, order):
        breed = json.loads(input)
        breed = jsonpickle.decode(breed)
        outcomeList = []
        for item in breed:
            outcomeList.append(item[order])

        return outcomeList

    def GetOutcome(self):
        try:
            print("sending ...")
            self.controller.in_out_server.write("OUTCOMETYPE\n")
            self.controller.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.controller.in_out_server.readline().rstrip('\n')
            outcomeList = self.ProcessData(answer, "OutcomeType")

            figureOutcome = plt.figure(figsize=(6, 6))
            plt.title("Outcome")
            figureOutcome.autofmt_xdate(rotation=90)
            plt.gcf().canvas.draw()
            histogram = plt.hist(outcomeList)
            histogram = FigureCanvasTkAgg(figureOutcome, self)
            histogram.get_tk_widget().place(relx=0.03, rely=0.15, relheight=0.80, relwidth=0.2275)
            print("Done!")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def GetSexuponOutcome(self):
        try:
            print("sending ...")
            self.controller.in_out_server.write("SEXUPONOUTCOME\n")
            self.controller.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.controller.in_out_server.readline().rstrip('\n')
            SexuponOutcomeList = self.ProcessData(answer, "SexuponOutcome")

            figureSexuponOutcome = plt.figure(figsize=(6, 6))
            plt.title("Sex")
            figureSexuponOutcome.autofmt_xdate(rotation=90)
            plt.gcf().canvas.draw()
            histogram = plt.hist(SexuponOutcomeList)
            histogram = FigureCanvasTkAgg(figureSexuponOutcome, self)
            histogram.get_tk_widget().place(relx=0.2675, rely=0.15, relheight=0.80, relwidth=0.2275)
            print("Done!")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def GetAgeuponOutcome(self):
        try:
            print("sending ...")
            self.controller.in_out_server.write("AGEUPONOUTCOME\n")
            self.controller.in_out_server.flush()
            print("waiting for answer ... ")
            answer = self.controller.in_out_server.readline().rstrip('\n')
            AgeuponOutcomeList = self.ProcessData(answer, "AgeuponOutcome")

            figureAgeuponOutcome = plt.figure(figsize=(6, 6))
            plt.title("Age")
            figureAgeuponOutcome.autofmt_xdate(rotation=90)
            plt.gcf().canvas.draw()
            histogram = plt.hist(AgeuponOutcomeList)
            histogram = FigureCanvasTkAgg(figureAgeuponOutcome, self)
            histogram.get_tk_widget().place(relx=0.505, rely=0.15, relheight=0.80, relwidth=0.2275)
            print("Done!")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.controller.in_out_server.write("%s\n" % "CLOSE")
            self.controller.in_out_server.flush()
            self.controller.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("AnimalShelterServer", "Something has gone wrong...")


class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, bg='#6bdbb2')
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = Frame(frame, bg='#31ad80')
        card.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)

        title = Label(card, text='SIGN IN', bg='#31ad80', fg='white')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)

        email_lbl = Label(card, text='Email', bg='#31ad80', fg='white', anchor="w")
        email_lbl.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.0266)
        self.email = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3')
        self.email.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.08)

        password_lbl = Label(card, text='Password', bg='#31ad80', fg='white', anchor="w")
        password_lbl.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.0266)
        self.password = Entry(card, text='Login', fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3', show="*")
        self.password.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.08)

        self.textError = StringVar()
        self.textError.set("")
        error = Label(card, textvariable=self.textError, bg='#31ad80', fg='white')
        error.place(relx=0.1, rely=0.60, relwidth=0.8, relheight=0.1)

        login = Button(card, text='SIGN IN', fg='white', bg='#018555', bd=0, activebackground='#016943', activeforeground='white', command=lambda: self.login())
        login.place(relx=0.1, rely=0.70, relwidth=0.8, relheight=0.08)

        register = Button(card, text='Create an account', fg='white', bg='#31ad80', bd=0, command=lambda: self.goToRegister())
        register.place(relx=0.1, rely=0.90, relwidth=0.8, relheight=0.08)

    def goToRegister(self):
        self.textError.set("")
        self.controller.showFrame(Register)

    def login(self):
        try:

            email = self.email.get()
            password = self.password.get()

            if email != '' and password != '':
                loginDict = {}
                user = User(email=email, password=password, nickname="", name="")
                jsonuser = jsonpickle.encode(user)
                loginDict["type"] = "LOGIN_RESPONSE"
                loginDict["value"] = jsonuser
                self.controller.in_out_server.write("%s \n" % json.dumps(loginDict))
                logging.info("Sending password: User")
                print(json.dumps(loginDict))
                self.controller.in_out_server.flush()

                # waiting for answer
                result = self.controller.in_out_server.readline().rstrip('\n')
                logging.info("Result server: %s" % result)

                if result == 'OK':
                    self.email.delete(0, END)
                    self.password.delete(0, END)
                    self.controller.showFrame(Applicatie)
                elif result == 'NOK':
                    pass
                    # Error handeling
                else:
                    raise Exception
            else:
                self.textError.set("Please fill in all fields")

        except Exception as ex:
            logging.error("Error: %s" % ex)
            messagebox.showinfo("SignIn", "Something has gone wrong...")


class Register(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.createdom()

    def createdom(self):

        frame = Frame(self, bg='#6bdbb2')
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = Frame(frame, bg='#31ad80')
        card.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)

        title = Label(card, text='REGISTER', bg='#31ad80', fg='white')
        title.place(relx=0.1, rely=0.05, relwidth=0.8)

        username_lbl = Label(card, text='Username', bg='#31ad80', fg='white', anchor="w")
        username_lbl.place(relx=0.1, rely=0.10, relwidth=0.8, relheight=0.0266)
        self.username = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3')
        self.username.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.08)

        email_lbl = Label(card, text='Email', bg='#31ad80', fg='white', anchor="w")
        email_lbl.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.0266)
        self.email = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3')
        self.email.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.08)

        nickname_lbl = Label(card, text='Nickname', bg='#31ad80', fg='white', anchor="w")
        nickname_lbl.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.0266)
        self.nickname = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3')
        self.nickname.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.08)

        password_lbl = Label(card, text='Password', bg='#31ad80', fg='white', anchor="w")
        password_lbl.place(relx=0.1, rely=0.70, relwidth=0.3, relheight=0.0266)
        self.password = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3', show="*")
        self.password.place(relx=0.1, rely=0.75, relwidth=0.375, relheight=0.08)

        repeatPassword_lbl = Label(card, text='Repeat Password', bg='#31ad80', fg='white', anchor="w")
        repeatPassword_lbl.place(relx=0.525, rely=0.70, relwidth=0.3, relheight=0.0266)
        self.repeatPassword = Entry(card, fg='black', bg='#D4D4D4', bd=0, selectbackground='#6c64d3', show="*")
        self.repeatPassword.place(relx=0.525, rely=0.75, relwidth=0.375, relheight=0.08)

        self.textError = StringVar()
        self.textError.set("")
        error = Label(card, textvariable=self.textError, bg='#31ad80', fg='white')
        error.place(relx=0.1, rely=0.83, relwidth=0.8, relheight=0.1)

        login = Button(card, text='Login', fg='white', bg='#31ad80', bd=0, command=lambda: self.goToLogin())
        login.place(relx=0.1, rely=0.90, relwidth=0.375, relheight=0.08)

        register = Button(card, text='SIGN UP', fg='white', bg='#018555', bd=0, activebackground='#016943', activeforeground='white', command=lambda: self.register())
        register.place(relx=0.525, rely=0.90, relwidth=0.375, relheight=0.08)

    def goToLogin(self):
        self.textError.set("")
        self.controller.showFrame(Login)

    def register(self):
        try:
            username = self.username.get()
            password = self.password.get()
            repeatpassword = self.repeatPassword.get()
            email = self.email.get()
            nickname = self.nickname.get()

            if username != '' and password != '' and repeatpassword != '' and email != '' and nickname != '':
                if password == repeatpassword:
                    registerDict = {}
                    user = User(email=email, password=password, nickname=nickname, name=username)
                    jsonuser = jsonpickle.encode(user)
                    registerDict["type"] = "REGISTER_RESPONSE"
                    registerDict["value"] = jsonuser
                    self.controller.in_out_server.write("%s \n" % json.dumps(registerDict))
                    self.controller.in_out_server.flush()

                    # waiting for answer
                    result = self.controller.in_out_server.readline().rstrip('\n')
                    logging.info("Result server: %s" % result)

                    if result == 'OK':
                        self.controller.showFrame(Applicatie)
                        self.textError.set("")
                    elif result == 'NOK':
                        # Error handeling
                        result = self.controller.in_out_server.readline().rstrip('\n')
                        self.textError.set(result)
                else:
                    # Error handeling !!
                    self.textError.set("Passwords aren't the same")
            else:
                # Error handeling !!
                self.textError.set("Please fill in all the fields")

        except Exception as ex:
            logging.error("Error: %s" % ex)
            messagebox.showinfo("SignIn", "Something has gone wrong...")


logging.basicConfig(level=logging.INFO)
root = Client()
root.geometry("1900x1080")
root.mainloop()
