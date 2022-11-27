import tkinter as tk
from tkinter import ttk

class ChatFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Grid layout setup
        self.columnconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # Chat Window Title
        self.chatWindowTitle = tk.Frame(master=self, borderwidth=1)
        self.chatWindowTitle.grid(row=0, column=2)
        self.chatWindowLabel = tk.Label(self.chatWindowTitle, text=f'\n SuperSecretFirstChat')
        self.chatWindowLabel.pack(side=tk.TOP)

        # Group Window Title
        self.groupWindowTitle = tk.Frame(master=self, borderwidth=1)
        self.groupWindowTitle.grid(row=0, column=0)
        self.groupWindowLabel = tk.Label(self.groupWindowTitle, text=f'\n Groups')
        self.groupWindowLabel.pack(side=tk.LEFT)

        # Options button
        self.optionWindow = tk.Frame(master=self, borderwidth=1)
        self.optionWindow.grid(row=0, column=4)
        self.optionButton = tk.Button(self.optionWindow, text="Options",
                                      command=self.advanced_options, bg="#211a52", fg="white")
        self.optionButton.pack(side=tk.RIGHT)

        # Group Window
        self.groupWindow = tk.Frame(master=self, borderwidth=1)
        self.groupWindow.grid(row=1,column=1,ipady=50,sticky=tk.NW)
        self.scrollbar = tk.Scrollbar(self.groupWindow, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.groupList = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.groupList.insert(1, "Create group")
        self.groupList.grid(row=1,column=0,ipady=50,sticky=tk.NW)
        self.scrollbar.config(command=self.groupList.yview)

        # Chat Window
        self.chatWindow = tk.Frame(master=self,borderwidth=1)
        self.chatWindow.grid(row=1,column=2,ipady=50,sticky=tk.NW)
        self.chat = tk.Text(self.chatWindow)
        self.chat.pack(side=tk.TOP)
        self.chat.config(state=tk.DISABLED)

        # Msg Input Window
        self.userInput = tk.StringVar()
        self.inputField = tk.Entry(self.chatWindow, text=self.userInput)
        self.inputField.pack(side=tk.TOP,fill=tk.X)

        self.inputField.bind("<Return>", self.sendMsg)
        self.groupList.bind("<<ListboxSelect>>", self.changeGroup)

    def sendMsg(self, event):
        msgInput = self.inputField.get()
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.INSERT, 'Me: %s\n' % msgInput)
        self.chat.config(state=tk.DISABLED)
        self.userInput.set('')

    def changeGroup(self, event):
        selection = event.widget.curselection()
        fieldSelect = event.widget.get(selection)
        if fieldSelect == "Create group":
            print("You are now creating a new group")
            self.newGroup()
        elif selection:
            pass
        else:
            print("Error") 

    def newGroup(self):
        self.popup = tk.Toplevel(self)
        self.popup.geometry("500x250")
        self.popup.resizable(0, 0)
        self.popup.title("Create group")

        self.labelFrame = tk.Frame(master=self.popup)
        self.labelFrame.grid(row=0, column=0)
        tk.Label(self.labelFrame, text="Group name").pack(side=tk.TOP)

        self.entryFrame = tk.Frame(master=self.popup)
        self.entryFrame.grid(row=0, column=1)
        self.groupName = tk.StringVar()
        self.groupNameInput = tk.Entry(self.entryFrame, width=25, text=self.groupName)
        self.groupNameInput.pack()

        self.groupNameInput.bind("<Return>", self.createGroup)
        
    def createGroup(self, event):
        groupName = self.groupNameInput.get()
        print("Creating group with name: {}".format(groupName))
        self.groupList.insert(0, "%s" % groupName)
        self.popup.destroy()
        
    def advanced_options(self):
        pass

class MainFrame(tk.Tk):
    def __init__(self):
        """Initialize root window"""
        super().__init__()

        # Window configuration
        self.geometry("1000x550")
        self.resizable(0,0)
        self.title("EncryptedChat")
        self.state("normal")

        self.__crate_widgets()



    def __crate_widgets(self):
        chat_window = ChatFrame(self)
        chat_window.grid(column=0, row=0)

if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()
