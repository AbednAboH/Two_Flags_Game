import tkinter as tk
from tkinter import *
from tkinter import ttk
class App:
    # 'what' and 'why' should probably be fetched in a different way, suitable to the app
    def __init__(self, root):
        self.parent = root
        self.parent.title("Flags Game")
        self.ip_address=""
        self.port_number=""
        self.Timer=""
        self.agentLabel2=tk.Label(root, text=" agent vs agent:").grid(row=1)
        self.agentLabel=tk.Label(root, text="agent: ").grid(row=2)
        self.humanLabel=tk.Label(root, text="human:").grid(row=3)
        self.serverLabel=tk.Label(root, text="server vs agent:").grid(row=4)
        self.agent1 = tk.IntVar()
        self.agent2 = tk.IntVar()
        self.human1 = tk.IntVar()
        self.server = tk.IntVar()
        tk.Checkbutton(root, text="agent vs agent", variable=self.agent1).grid(row=1, column=1, sticky=tk.W)
        self.agent = tk.Scale(root, from_=True, to=False, orient="horizontal",variable=self.agent2).grid(row=2,column=1)
        self.human= tk.Scale(root, from_=True, to=False, orient="horizontal",variable=self.human1).grid(row=3,column=1)
        tk.Checkbutton(root, text="put server ip and socket number", variable=self.server).grid(row=6, column=1, sticky=tk.W)
        tk.Label(root, text="Add Time ").grid(row=7)
        tk.Label(root, text="Setup").grid(row=8)
        tk.Label(root, text="Server Address(ip)").grid(row=9)
        tk.Label(root, text="port number").grid(row=10)
        self.ip = tk.Entry(self.parent)
        self.port = tk.Entry(self.parent)
        self.time = tk.Entry(self.parent)
        self.setup = tk.Entry(self.parent)
        self.ip.grid(row=9, column=1)
        self.port.grid(row=10, column=1)
        self.time.grid(row=7, column=1)
        self.setup.grid(row=8, column=1)
        tk.Button(root, text='apply', command=self.use_entry).grid(row=11, column=1, sticky=tk.W, pady=4)
    def use_entry(self):
        self.ip_address = self.ip.get()
        self.port_number = self.port.get()
        self.Timer=self.time.get()
        self.Setup=self.setup.get()
        self.parent.destroy() # if you must