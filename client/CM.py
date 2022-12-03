import socket
import select
import sys

import threading
import argparse
import GUI_Base

class ChatManager:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-ip', type=str, required=False)
        parser.add_argument('-port', type=int, required=False)
        args = parser.parse_args()
        self.IP_address = str(args.ip) if args.ip else "127.0.0.1"
        self.Port = int(args.port) if args.port else 9000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.IP_address, self.Port))
    
        print("Connected to server")
        self.gui = GUI_Base.MainFrame(self)
        print(self.gui.chat_window.dummy())
        

    def start_thread(self):
        new_thread = threading.Thread(name="ChatManager Thread", target=self.listen, args=())
        new_thread.start()
        return new_thread

    def listen(self):
        print(self.gui.chat_window.dummy())
        while True:
            try:
                msg = self.server.recv(2048)
                #self.gui.chat_window.recv_msg(msg)
            except OSError:
                print(OSError)
                break

            
    def hello(self):
        print("Hello")
        

if __name__ == "__main__":
    cm = ChatManager()
    cm.gui.mainloop()
