# Serverside ChatManager (Main Program)
import socket
import select
import sys
from _thread import *
import argparse
from datetime import datetime

# sep = chr(31)
sep = "chr(31)"

class ChatManager:
    # Argument Parsing Setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, required=False)
    parser.add_argument('-port', type=int, required=False)
    args = parser.parse_args()

    """The first argument AF_INET is the address domain of the
    socket. This is used when we have an Internet Domain with
    any two hosts The second argument is the type of socket.
    SOCK_STREAM means that data or characters are read in
    a continuous flow."""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    # takes the IP argument from command prompt as IP address, if any exists
    IP_address = str(args.ip) if args.ip else "127.0.0.1"

    # takes Port argument from command prompt as port number, if any exists
    Port = int(args.port) if args.port else 9000


    print(f"Readied IP is: {IP_address}")
    print(f"Readied Port is: {Port}")

    """
    binds the server to an entered IP address and at the
    specified port number.
    The client must be aware of these parameters
    """
    server.bind((IP_address, Port))

    """
    listens for 100 active connections. This number can be
    increased as per convenience.
    """
    server.listen(100)

    print("Server started.")
    print(f"Server IP is: {IP_address}")
    print(f"Server Port is: {Port}")


    list_of_clients = []

    def handle_incoming_msg(self, conn, alias, group_id, payload):

        dt = datetime.now()             # time - human format
        ts = datetime.timestamp(dt)     # time - computer format

        # !!!!!!!!!! log to database

        Header = "1"+"|"+str(alias)+"|"+str(group_id)+"|"
        packet = bytes(Header + payload + "|" + str(dt), 'utf-8')
        print("Broadcasted message: " + str(packet))
        self.broadcast(packet, conn)


    def recv_and_sort(self, message, conn):
        packet = str(message.decode('utf8'))
        list = packet.split("|")

        if list[0] == '0':
            alias = list[1]
            group_id = list[2]
            payload = list[3]
            self.handle_incoming_msg(conn, alias, group_id, payload)

        elif list[0] == '2':
            pass
        elif list[0] == '3':
            pass
        elif list[0] == '4':
            pass
        elif list[0] == '5':
            pass
        elif list[0] == '6':
            pass
        elif list[0] == '7':
            pass

    def clientthread(self, conn, addr):

        # sends a message to the client whose user object is conn
        conn.send(b"Welcome to this chatroom!")

        while True:
                try:
                    message = conn.recv(2048)
                    if message:
                        print("Received message from client")
                        """prints the message and address of the
                        user who just sent the message on the server
                        terminal"""
                        print ("<" + addr[0] + "> " + message.decode('utf-8'))

                        # packet= str(message.decode('utf-8'))
                        # list = packet.split("|")

                        self.recv_and_sort(message, conn)


                        # Calls broadcast function to send message to all
                        # message_to_send = "<" + addr[0] + "> " + message
                        #message_to_send = "<" + addr[0] + "> " + payload
                        #print('Message to send to other users:')
                        #print(message_to_send)
                        #self.broadcast(message_to_send, conn)
                        #print(f"Separator from ClientThread is: {sep}")


                    else:
                        """message may have no content if the connection
                        is broken, in this case we remove the connection"""
                        self.remove(conn)

                except:
                    continue



    """Using the below function, we broadcast the message to all
    clients who's object is not the same as the one sending
    the message """
    def broadcast(self, message, connection):
        print("Clients to send to: ")
        print(len(self.list_of_clients))
        print(f"Separator from Broadcast is: {sep}")


        for clients in self.list_of_clients:		# For everyone in the chat
            if clients != connection:			# Unless it's the sender themself
                dir(clients)
                # print(f'Message sent to client {clients}')
                try:
                    clients.send(message)
                except:
                    print("Didn't send to client " + clients)
                    clients.close()

                    # if the link is broken, we remove the client
                    self.remove(clients)

        print(f"Separator from Broadcast is: {sep}")


    """The following function simply removes the object
    from the list that was created at the beginning of
    the program"""
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)


    def listener(self):
        while True:

            """Accepts a connection request and stores two parameters,
            conn which is a socket object for that user, and addr
            which contains the IP address of the client that just
            connected"""
            self.conn, addr = self.server.accept()

            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""
            self.list_of_clients.append(self.conn)

            # prints the address of the user that just connected
            print (addr[0] + " connected")

            # creates and individual thread for every user
            # that connects
            start_new_thread(self.clientthread,(self.conn,addr))

        conn.close()
        server.close()


if __name__ == "__main__":
    cm = ChatManager()
    cm.listener()
