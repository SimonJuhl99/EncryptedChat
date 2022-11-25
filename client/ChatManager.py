# Python program to implement client side of chat room.
import socket
import select
import sys
# from _thread import *
import threading
import argparse
import GUI

# sep = chr(31)
sep = "chr(31)"
user_id = 1
group_id = 42



class ChatManager:

    def __init__(self,ip,port,parent=None):

        self.parent = parent
        self.IP_address = str(ip) if ip else "127.0.0.1"
        self.Port = int(port) if port else 9000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.IP_address, self.Port))

    def start_thread(self):
        # new_thread = threading.Thread(name="GUI Thread", target=gui.mainloop, args=())
        #new_thread = threading.Thread(name="ChatManager Thread", target=self.run, args=())
        new_thread = threading.Thread(name="ChatManager Thread", target=self.recv, args=())
        new_thread.start()
        return new_thread


    def first_fetch(self):
        # get all group objects from database
        pass

    def handle_message(self, payload, alias, group_id):
        # send text to all users in the group with group_id
        #self.server.send(bytes(text + ":" + group_id + ":" + alias, 'utf-8'))
        Header = "0"+"|"+str(alias)+"|"+str(group_id)+"|"
        packet = bytes(Header + payload, 'utf-8')
        self.server.send(packet)


    def recv(self):
        while True:
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, self.server]

            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(2048)
                    # print('Modtaget noget fra server:')
                    self.parent.recv_msg(message)


    def create_group(self):
        pass

    def join_group(self, invite_code):
        pass

    def leave_group(self, group_id):
        pass

    def authenticate():
        pass

    def build_frame(self, payload, user_id, group_id):
        Header = "0"+"|"+str(user_id)+"|"+str(group_id)+"|"
        packet = bytes(Header + payload, 'utf-8')
        return packet

    def run(self):
        while True:
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, self.server]

            """ There are two possible input situations. Either the
            user wants to give manual input to send to other people,
            or the server is sending a message to be printed on the
            screen. Select returns from sockets_list, the stream that
            is reader for input. So for example, if the server wants
            to send a message, then the if condition will hold true
            below.If the user wants to send a message, the else
            condition will evaluate as true"""
            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(2048)
                    # print('Modtaget noget fra server:')
                    print (message.decode('utf-8'))

                else:
                    payload = sys.stdin.readline()
                    #Header = "0"+"|"+str(user_id)+"|"+str(group_id)+"|"
                    #packet = bytes(Header + payload, 'utf-8')
                    packet = self.build_frame(payload, user_id, group_id)
                    self.server.send(packet)


        server.close()




if __name__ == "__main__":
    # Argument Parsing Setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, required=False)
    parser.add_argument('-port', type=int, required=False)
    args = parser.parse_args()
    # Initiate Objects
    cm = ChatManager(args.ip, args.port)
    # gui = GUI.HomeScreen("Nisse")

    # thread = threading.Thread(name="GUI Thread", target=gui.mainloop(), args=())
    # thread.start()
    # cm.start_thread()

    # start_new_thread(gui.mainloop(), *args)
    # start_new_thread(cm.run())


    # gui.mainloop()
    cm.run()
