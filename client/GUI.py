import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import argparse
import ChatManager
import User


class GroupName():
    def __init__(self, group_name):
        self.group_name = group_name


class HomeScreen(tk.Tk):
    def __init__(self, group_name):
        super().__init__()
        self.cm = ChatManager.ChatManager(args.ip,args.port,self)
        self.active_group = None
        self.geometry("1000x550")
        self.resizable(0,0)
        self.group = GroupName(group_name)
        self.title("Encrypted Chat")
        self.frame1 = tk.Frame(master=self,borderwidth=1)
        self.frame1.grid(row=0,column=2)
        self.title_label = tk.Label(self.frame1,
            text=f'\n {self.group.group_name}'
        )
        self.title_label.pack(side=tk.TOP)                                 #Places title label in cneter

        self.frame2 = tk.Frame(master=self, borderwidth=1)
        self.frame2.grid(row=0,column=0)
        self.group_label = tk.Label(self.frame2,
            text=f'\n Groups')
        self.group_label.pack(side=tk.LEFT)
        self.frame3 = tk.Frame(master=self, borderwidth=1)
        self.frame3.grid(row=0,column=4)
        self.advanced_button = tk.Button(self.frame3,text="Options",command=self.advanced_options, bg="#211A52", fg = "white")
        self.advanced_button.pack(side=tk.RIGHT)

        self.frame4 = tk.Frame(master=self,borderwidth=1)
        self.frame4.grid(row=1,column=1,ipady=50,sticky=tk.NW)
        self.scrollbar = tk.Scrollbar(self.frame4, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill = Y)
        self.mylist = Listbox(self,yscrollcommand=self.scrollbar.set)

        for line in range(1,101):
            self.mylist.insert(END,"Group"+ str(line))

        first_list_item_tuple = self.mylist.get(0, 0)                   # we retrieve the first element of the ListBox "mylist"
        for first_list_item in first_list_item_tuple:
            first_group_name = first_list_item.split(" ")[0]            # we retrieve the groupname from that element

        self.set_active_group(first_group_name)
        self.mylist.grid(row=1,column=0,ipady=50,sticky=tk.NW)
        self.scrollbar.config(command=self.mylist.yview)

        self.frame5 = tk.Frame(master=self,borderwidth=1)
        self.frame5.grid(row=1,column=2,ipady=50,sticky=tk.NW)
        self.chat_window = tk.Text(self.frame5)
        self.chat_window.pack(side=TOP)
        self.chat_window.config(state=DISABLED)

        self.input_user = StringVar()
        self.input_entry = Entry(self.frame5, text=self.input_user)
        self.input_entry.pack(side=TOP,fill=X)

        self.input_entry.bind("<Return>", self.send_msg)
        self.mylist.bind("<<ListboxSelect>>",self.trigger) #binding mylist widget to the trigger event

    def recv_msg(self,data):
        print(data.decode('utf-8'))
        decoded_data = data.decode('utf-8')
        self.chat_window.config(state=NORMAL)
        self.chat_window.insert(INSERT, '%s\n' % decoded_data)
        self.chat_window.config(state=DISABLED)

    def send_msg(self, event):
        input_get = self.input_entry.get()
        my_message = "Me: " + input_get
        self.chat_window.config(state=NORMAL)
        self.chat_window.insert(INSERT, '%s\n' % my_message)
        self.chat_window.config(state=DISABLED)
        self.input_user.set('')
        self.cm.handle_message(input_get,self.active_group,usr.get_alias())
        return "break"


    def trigger(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.title_label.configure(text=data)
            self.chat_window.configure()
            self.chat_window.delete(1.0,tk.END)
        else:
            self.title_label.configure(text="Error")



    def advanced_options(self):
        #empty for now
        self.name() #doesn't work but needs to be there

    def set_active_group(self, group_id):
        self.active_group = group_id







if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, required=False)
    parser.add_argument('-port', type=int, required=False)
    args = parser.parse_args()


    chat_window = HomeScreen("Secret Service")
    #cm = ChatManager.ChatManager(args.ip,args.port,self)
    usr = User.User(10224892379847824, "Løg", "hej1234")
    chat_window.cm.start_thread()
    chat_window.mainloop()
