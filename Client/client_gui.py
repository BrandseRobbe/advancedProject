import logging
import socket
from threading import Thread
from tkinter import *
from tkinter import messagebox
import jsonpickle
import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Models.User import User
import tkinter.font as tkFont
from tkinter import ttk
import time
from csv import reader
import pandas as pd

textcolor = "#00008b"
inputcolor = "#f0f6ff"
light = "#f0f6ff"
framecolor ="#e0edff"
button = "#d6e7ff"
button_active = "#b3d2ff"
pressed_button = "#b3d2ff"
dark = "#adceff"


class Client(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.userData = None

        self.outcometypedata = None
        self.choicesBreedData = None
        self.choicesColorData = None
        self.choicesAgeData = None
        self.color = None
        self.age = None
        self.breed = None
        self.name = None
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
        self.showFrame(Login)

    def logOut(self):
        print("logout attempt")
        if self.userData is not None:
            # use was logged in => send logout
            print(self.userData)
            self.sendMessageToServer("LOGOUT_USER", jsonpickle.encode(self.userData))
            self.userData = None
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

    def sendMessageToServer(self, messageType, messageValue=""):
        message = {"type": messageType, "value": messageValue}
        self.in_out_server.write("%s \n" % json.dumps(message))
        self.in_out_server.flush()
        print("just sent: %s" % message)

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
            elif messagetype == "BREEDDROPDOWN":
                self.handleBreedDropdown(messagevalue)
            elif messagetype == "COLORDROPDOWN":
                self.handleColorDropdown(messagevalue)
            elif messagetype == "AGEDROPDOWN":
                self.handleAgeDropdown(messagevalue)
            elif messagetype == "ANIMALCOLOR":
                self.handleColor(messagevalue)
            elif messagetype == "ANIMALAGE":
                self.handleAge(messagevalue)
            elif messagetype == "ANIMALBREED":
                self.handleBreed(messagevalue)
            elif messagetype == "ANIMALNAME":
                self.handleName(messagevalue)

    def handleName(self, value):
        print(value)
        self.name = value

    def handleBreed(self, value):
        self.breed = value

    def handleAge(self, value):
        self.age = value

    def handleColor(self, value):
        self.color = value

    def handleAgeDropdown(self, value):
        self.choicesAgeData = value

    def handleColorDropdown(self, value):
        self.choicesColorData = value

    def handleBreedDropdown(self, value):
        self.choicesBreedData = value

    def handleOutcometype(self, value):
        self.outcometypedata = value

    def handleRegister(self, allowed):
        if allowed:
            print("register succesfull")
            self.showFrame(Applicatie)

    def handleLogin(self, allowed):
        if allowed:
            self.showFrame(Applicatie)


    def handleAlert(self, message):
        print("!!! %s !!!" % message)

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
        self.buttonOutcome = Button(self.frame, text="Get outcome", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Outcome))
        # self.buttonOutcome = Button(self.frame, text="Get outcome", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.navigation("outcometype"))
        self.buttonOutcome.place(relx=0.142857, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonName = Button(self.frame, text="Search animal by name", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Name))
        self.buttonName.place(relx=0.285714, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonBreed = Button(self.frame, text="Search animal by breed", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Breed))
        self.buttonBreed.place(relx=0.428571, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonColor = Button(self.frame, text="Search animal by color", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Color))
        self.buttonColor.place(relx=0.571428, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonAge = Button(self.frame, text="Search animal by Age", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.showFrame(Age))
        self.buttonAge.place(relx=0.714285, rely=0.0, relheight=0.05, relwidth=0.142857)
        self.buttonLogin = Button(self.frame, text="Logout", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.controller.logOut())
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
        input_lbl = Label(self.frame, text='Name', bg=light, fg='black', anchor="w")
        input_lbl.place(relx=0.3, rely=0.06, relwidth=0.05, relheight=0.05)
        self.input = Entry(self.frame, fg='black', bg=dark, bd=0, selectbackground=dark)
        self.input.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.30)

        self.buttonSubmit = Button(self.frame, text="Search", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.submit())
        self.buttonSubmit.place(relx=0.60, rely=0.1, relheight=0.05, relwidth=0.10)

        self.list = Listbox(self.frame)
        self.list.place(relx=0.25, rely=0.2, relheight=0.75, relwidth=0.50)

    def submit(self):
        self.list.delete(0, END)
        self.controller.sendMessageToServer("ANIMALNAME", self.input.get())
        name = self.controller.name
        while (name == None):
            time.sleep(0.3)
            name = self.controller.name

        if name == "No animals found":
            self.list.insert(0, "No animals found please try another name.")
        else:
            name = json.loads(name)
            teller = 0
            for item in name:
                self.list.insert(teller, "%s          -          %s          -          %s" % (item[0], item[1], item[2]))
                teller += 1
        self.controller.name = None


class Breed(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonBreed.configure(bg=button_active)
        print("sending request breeddropdown")
        self.controller.sendMessageToServer("BREEDDROPDOWN")
        print("waiting for answer ... ")
        choices = self.controller.choicesBreedData
        while (choices == None):
            time.sleep(0.3)
            choices = self.controller.choicesBreedData
        print("choices")
        print(choices)
        self.BreedDropdown = ttk.Combobox(self.frame, width=15, state="readonly")
        self.BreedDropdown['values'] = choices
        self.BreedDropdown.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.30)

        self.buttonSubmit = Button(self.frame, text="Search", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.submit())
        self.buttonSubmit.place(relx=0.60, rely=0.1, relheight=0.05, relwidth=0.10)

        self.list = Listbox(self.frame)
        self.list.place(relx=0.25, rely=0.2, relheight=0.75, relwidth=0.50)

    def submit(self):
        self.list.delete(0, END)
        self.controller.sendMessageToServer("ANIMALBREED", self.BreedDropdown.get())
        breed = self.controller.breed
        while (breed == None):
            time.sleep(0.3)
            breed = self.controller.breed
        breed = json.loads(breed)
        teller = 0
        for item in breed:
            self.list.insert(teller, "%s          -          %s          -          %s" % (item[0], item[1], item[2]))
            teller += 1
        self.controller.breed = None


class Color(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonColor.configure(bg=button_active)

        print("sending request colordropdown")
        self.controller.sendMessageToServer("COLORDROPDOWN")
        print("waiting for answer ... ")
        choices = self.controller.choicesColorData
        while (choices == None):
            time.sleep(0.3)
            choices = self.controller.choicesColorData
        print("choices")
        print(choices)
        self.ColorDropdown = ttk.Combobox(self.frame, width=15, state="readonly")
        self.ColorDropdown['values'] = choices
        self.ColorDropdown.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.30)

        self.buttonSubmit = Button(self.frame, text="Search", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.submit())
        self.buttonSubmit.place(relx=0.60, rely=0.1, relheight=0.05, relwidth=0.10)

        self.list = Listbox(self.frame)
        self.list.place(relx=0.25, rely=0.2, relheight=0.75, relwidth=0.50)

    def submit(self):
        self.list.delete(0, END)
        self.controller.sendMessageToServer("ANIMALCOLOR", self.ColorDropdown.get())
        color = self.controller.color
        while (color == None):
            time.sleep(0.3)
            color = self.controller.color
        color = json.loads(color)
        teller = 0
        for item in color:
            self.list.insert(teller, "%s          -          %s" % (item[0], item[1]))
            teller += 1
        self.controller.color = None


class Age(Navigation):
    def __init__(self, parent, controller):
        Navigation.__init__(self, parent, controller)
        self.controller = controller
        # controller = self van client
        self.buttonAge.configure(bg=button_active)
        print("sending request agedropdown")
        self.controller.sendMessageToServer("AGEDROPDOWN")
        print("waiting for answer ... ")
        choices = self.controller.choicesAgeData
        while (choices == None):
            time.sleep(0.3)
            choices = self.controller.choicesAgeData
        print("choices")
        print(choices)
        self.AgeDropdown = ttk.Combobox(self.frame, width=15, state="readonly")
        self.AgeDropdown['values'] = choices
        self.AgeDropdown.place(relx=0.3, rely=0.1, relheight=0.05, relwidth=0.30)

        self.buttonSubmit = Button(self.frame, text="Search", bg=button, activebackground=pressed_button, borderwidth=0, command=lambda: self.submit())
        self.buttonSubmit.place(relx=0.60, rely=0.1, relheight=0.05, relwidth=0.10)

        self.list = Listbox(self.frame)
        self.list.place(relx=0.25, rely=0.2, relheight=0.75, relwidth=0.50)

    def submit(self):
        self.list.delete(0, END)
        self.controller.sendMessageToServer("ANIMALAGE", self.AgeDropdown.get())
        age = self.controller.age
        while (age == None):
            time.sleep(0.3)
            age = self.controller.age
        age = json.loads(age)
        print("age")
        print(age)
        teller = 0
        for item in age:
            self.list.insert(teller, "%s          -          %s" % (item[0], item[1]))
            teller += 1
        self.controller.age = None


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
        self.createdom()

    def createdom(self):
        frame = Frame(self, bg=light)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = Frame(frame, bg=framecolor)
        card.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)

        title = Label(card, text='SIGN IN', bg=framecolor, fg=textcolor)
        title.place(relx=0.1, rely=0.08, relwidth=0.8)

        email_lbl = Label(card, text='Email', bg=framecolor, fg=textcolor, anchor="w")
        email_lbl.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.0266)
        self.email = Entry(card, fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3')
        self.email.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.08)

        password_lbl = Label(card, text='Password', bg=framecolor, fg=textcolor, anchor="w")
        password_lbl.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.0266)
        self.password = Entry(card, text='Login', fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3', show="*")
        self.password.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.08)

        self.textError = StringVar()
        self.textError.set("")
        error = Label(card, textvariable=self.textError, bg=framecolor, fg=textcolor)
        error.place(relx=0.1, rely=0.60, relwidth=0.8, relheight=0.1)

        login = Button(card, text='SIGN IN', fg=textcolor, bg=dark, bd=0, activebackground=button_active, activeforeground=textcolor, command=lambda: self.login())
        login.place(relx=0.1, rely=0.70, relwidth=0.8, relheight=0.08)

        register = Button(card, text='Create an account', fg='black', bg=framecolor, activebackground=framecolor ,bd=0, command=lambda: self.goToRegister())
        register.place(relx=0.1, rely=0.90, relwidth=0.8, relheight=0.08)

    def goToRegister(self):
        self.textError.set("")
        self.controller.showFrame(Register)

    def login(self):
        try:
            self.textError.set("")
            email = self.email.get()
            password = self.password.get()
            print("__ %s __" % password)
            if email != '' and password != '':
                if User.isValidPassword(password):
                    if User.isValidEmail(email):
                        user = User(email=email, password=password, nickname="", name="")
                        self.controller.userData = user
                        jsonuser = jsonpickle.encode(user)
                        self.controller.sendMessageToServer("LOGIN_ATTEMPT", jsonuser)
                    else:
                        self.textError.set("Invalid email format")
                else:
                    self.textError.set("Incorrect password")
            else:
                self.textError.set("Please fill in all fields")

        except Exception as ex:
            self.textError.set("Login failed")



class Register(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.createdom()

    def createdom(self):

        frame = Frame(self, bg=light)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = Frame(frame, bg=framecolor)
        card.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)

        title = Label(card, text='REGISTER', bg=framecolor, fg=textcolor)
        title.place(relx=0.1, rely=0.05, relwidth=0.8)

        username_lbl = Label(card, text='Username', bg=framecolor, fg=textcolor, anchor="w")
        username_lbl.place(relx=0.1, rely=0.10, relwidth=0.8, relheight=0.0266)
        self.username = Entry(card, fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3')
        self.username.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.08)

        email_lbl = Label(card, text='Email', bg=framecolor, fg=textcolor, anchor="w")
        email_lbl.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.0266)
        self.email = Entry(card, fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3')
        self.email.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.08)

        nickname_lbl = Label(card, text='Nickname', bg=framecolor, fg=textcolor, anchor="w")
        nickname_lbl.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.0266)
        self.nickname = Entry(card, fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3')
        self.nickname.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.08)

        password_lbl = Label(card, text='Password', bg=framecolor, fg=textcolor, anchor="w")
        password_lbl.place(relx=0.1, rely=0.70, relwidth=0.3, relheight=0.0266)
        self.password = Entry(card, fg=textcolor, bg=inputcolor, bd=0, selectbackground='#6c64d3', show="*")
        self.password.place(relx=0.1, rely=0.75, relwidth=0.375, relheight=0.08)

        repeatPassword_lbl = Label(card, text='Repeat Password', bg=framecolor, fg=textcolor, anchor="w")
        repeatPassword_lbl.place(relx=0.525, rely=0.70, relwidth=0.3, relheight=0.0266)
        self.repeatPassword = Entry(card, fg=textcolor, bg= inputcolor, bd=0, selectbackground='#6c64d3', show="*")
        self.repeatPassword.place(relx=0.525, rely=0.75, relwidth=0.375, relheight=0.08)

        self.textError = StringVar()
        self.textError.set("")
        error = Label(card, textvariable=self.textError, bg=framecolor, fg=textcolor)
        error.place(relx=0.1, rely=0.83, relwidth=0.8, relheight=0.1)

        login = Button(card, text='Login', fg=textcolor, bg=framecolor, activebackground=framecolor, bd=0, command=lambda: self.goToLogin())
        login.place(relx=0.1, rely=0.90, relwidth=0.375, relheight=0.08)

        register = Button(card, text='SIGN UP', fg=textcolor, bg=dark, bd=0, activebackground=button_active, activeforeground=textcolor, command=lambda: self.register())
        register.place(relx=0.525, rely=0.90, relwidth=0.375, relheight=0.08)

    def goToLogin(self):
        self.textError.set("")
        self.controller.showFrame(Login)

    def register(self):
        try:
            self.textError.set("")
            username = self.username.get()
            password = self.password.get()
            repeatpassword = self.repeatPassword.get()
            email = self.email.get()
            nickname = self.nickname.get()

            if username != '' and password != '' and repeatpassword != '' and email != '' and nickname != '':
                if password == repeatpassword:
                    if User.isValidPassword(password):
                        if User.isValidEmail(email):

                            user = User(email=email, password=password, nickname=nickname, name=username)
                            self.controller.userData = user
                            jsonuser = jsonpickle.encode(user)
                            self.controller.sendMessageToServer("REGISTER_ATTEMPT", jsonuser)
                        else:
                            self.textError.set("Invalid email format")
                    else:
                        self.textError.set("Password is too weak")
                else:
                    # Error handeling !!
                    self.textError.set("Passwords aren't the same")
            else:
                # Error handeling !!
                self.textError.set("Please fill in all the fields")

        except Exception as ex:
            self.textError.set("Email is already in use")


logging.basicConfig(level=logging.INFO)
root = Client()
root.geometry("1900x1080")
root.mainloop()
