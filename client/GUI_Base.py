import tkinter as tk

from ChatFrame import ChatFrame
import ChatManager

class MainFrame(tk.Tk):
    def __init__(self, cmRoot):
        """Initialize root window"""
        super().__init__()
        self.cm = cmRoot

        # Window configuration
        self.geometry("1000x550")
        self.resizable(0,0)
        self.title("EncryptedChat")
        self.state("normal")

        self.__crate_widgets()
        


    def __crate_widgets(self):
        chat_window = ChatFrame(self, self.cm)
        chat_window.grid(column=0, row=0)

        
if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()
