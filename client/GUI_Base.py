import tkinter as tk
from ChatFrame import *


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
