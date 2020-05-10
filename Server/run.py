from tkinter import *

from server_gui import ServerWindow
import os

def callback():
    print("callback")
    try:
        gui_server.afsluiten_server()
    except EXCEPTION:
        print('Nog niet opgestart')
    finally:
        print("destroy")
        root.destroy()
        print("destroy")
        os._exit(0)

root = Tk()
root.geometry("600x300")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
