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
import tkinter.font as tkFont
import time

light = "#f0f6ff"
button = "#d6e7ff"
button_active = "#b3d2ff"
pressed_button = "#b3d2ff"
dark = "#31ad80"


class Client(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.outcometypedata = None
        # Setup frame
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)

        self.makeConnectionWithServer()
        responseloop = Thread(target=self.getserverresponse)
        responseloop.start()
        self.frames = {}
        pages = [Login, Register, Applicatie, Outcome, Name, Breed, Color, Age]

        for f in pages:
            frame = f(container, self)
            self.frames[f] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.showFrame(Applicatie)

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

    def sendMessageToServer(self, messageType, messageValue=""):
        message = {"type": messageType, "value": messageValue}
        self.in_out_server.write("%s \n" % json.dumps(message))
        self.in_out_server.flush()

    def getserverresponse(self):
        print("starting response loop")
        loop = True
        while loop:
            # ontvangt van clienthandles
            jsonstring = self.in_out_server.readline().rstrip('\n')
            print("waiting for message ...")
            messageobj = json.loads(jsonstring)
            messagetype = messageobj["type"]
            messagevalue = messageobj["value"]
            if messagetype == "REGISTER_RESPONSE":
                self.handleRegister(messagevalue)
            elif messagetype == "LOGIN_RESPONSE":
                self.handleLogin(messagevalue)
            elif messagetype == "ALERT":
                self.handleAlert(messagevalue)
            elif messagetype == "OUTCOMETYPE":
                self.handleOutcometype(messagevalue)

    def handleOutcometype(self, value):
        self.outcometypedata = value

    def handleRegister(self, allowed):
        if allowed:
            print("register succesfull")
            self.showFrame(Applicatie)
            # self.textError.set("")
        else:
            # self.textError.set("Register failed")
            print("register not gud")
            raise EXCEPTION

    def handleLogin(self, allowed):
        if allowed:
            self.showFrame(Applicatie)
        else:
            # self.textError.set("Register failed")
            print("register not gud")
            raise EXCEPTION

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


class Navigation(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # controller = self van client
        self.showNav()

    def showNav(self):
        self.frame = Frame(self, bg=light)
        self.frame.place(relx='0', rely='0', relheight="1", relwidth="1")
        self.buttonApplicatie = Button(self.frame, text="AnimalShelter", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Applicatie))
        self.buttonApplicatie.place(relx=0.0, rely=0.0, relheight=0.05, relwidth=0.142857)
        # self.buttonOutcome = Button(self.frame, text="Get outcome", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Outcome))
        self.buttonOutcome = Button(self.frame, text="Get outcome", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.navigation("outcometype"))
        self.buttonOutcome.place(relx=0.142857, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonName = Button(self.frame, text="Search animal by name", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Name))
        self.buttonName.place(relx=0.285714, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonBreed = Button(self.frame, text="Search animal by breed", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Breed))
        self.buttonBreed.place(relx=0.428571, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonColor = Button(self.frame, text="Search animal by color", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Color))
        self.buttonColor.place(relx=0.571428, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonAge = Button(self.frame, text="Search animal by Age", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Age))
        self.buttonAge.place(relx=0.714285, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonLogin = Button(self.frame, text="Logout", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Login))
        self.buttonLogin.place(relx=0.857142, rely=0.0, relheight=0.05, relwidth=0.142857)

    def navigation(self, tab):
        if tab == "outcometype":
            # data ophaplen
            self.controller.showFrame(Outcome)


class Applicatie(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonApplicatie.configure(bg=button_active)

        title = Label(self.frame, text='Welcome', bg=light, fg='black')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)


class Name(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonName.configure(bg=button_active)

        title = Label(self.frame, text='Search animal by name', bg=light, fg='black')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)


class Breed(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonBreed.configure(bg=button_active)

        title = Label(self.frame, text='Search animal by breed', bg=light, fg='black')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)


class Color(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonColor.configure(bg=button_active)

        title = Label(self.frame, text='Search animal by color', bg=light, fg='black')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)


class Age(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonAge.configure(bg=button_active)

        title = Label(self.frame, text='Search animal by age', bg=light, fg='black')
        title.place(relx=0.1, rely=0.08, relwidth=0.8)


class Outcome(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonOutcome.configure(bg=button_active)

        self.pack(fill=BOTH, expand=1)
        self.GetOutcome()

    def GetOutcome(self):
        try:
            print("sending request outcometype")
            self.controller.sendMessageToServer("OUTCOMETYPE")
            print("waiting for answer ... ")
            outcomeList = self.controller.outcometypedata
            while (outcomeList == None):
                time.sleep(0.3)
                print("loop")
                outcomeList = self.controller.outcometypedata
            figureOutcome = plt.figure(figsize=(6, 6))
            plt.title("Outcome")
            plt.hist(outcomeList)
            figureOutcome.autofmt_xdate(rotation=90)
            plt.gcf().canvas.draw()
            histogram = FigureCanvasTkAgg(figureOutcome, self)
            histogram.get_tk_widget().place(relx=0.05, rely=0.15, relheight=0.75, relwidth=0.90)
            print("Done!")

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
            print("__ %s __" % password)
            if email != '' and password != '':
                user = User(email=email, password=password, nickname="", name="")
                jsonuser = jsonpickle.encode(user)
                self.controller.sendMessageToServer("LOGIN_ATTEMPT", jsonuser)
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
                    user = User(email=email, password=password, nickname=nickname, name=username)
                    jsonuser = jsonpickle.encode(user)
                    self.controller.sendMessageToServer("REGISTER_ATTEMPT", jsonuser)
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
