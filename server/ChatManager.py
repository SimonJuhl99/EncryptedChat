# Serverside ChatManager (Main Program)
import socket
import select
import sys
from _thread import *
import argparse
from datetime import datetime
from Database import *

sep = chr(31)
# sep = "|"

db = Database()

class ChatManager:


    def __init__(self, ip, port, parent=None):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((ip, port))
        self.server.listen(100)
        self.list_of_clients = []

        print("Server started.")
        print(f"Server IP is: {IP_address}")
        print(f"Server Port is: {Port}")




    def handle_incoming_msg(self, conn, user_id, group_id, payload):

        dt = datetime.now()             # time - human format
        ts = datetime.timestamp(dt)     # time - computer format
        time = dt.strftime("%d/%m-%y %H:%M:%S")

        params = {
            'text': payload, 
            'user_id': user_id, 
            'group_id': group_id, 
            'timestamp': time
        }
        db.insert('message', params)
        # db_config = {
        #     'where': {'id': user_id},
        #     'select': 'alias, ip',
        #     }
        # user = db.fetch('user', db_config)
        group = db.fetch_group_members(group_id)

        # print(group)
        group_ips = []
        current = 0
        print(f"\nIn Handle Message\nFetched data is:")
        for i, member in enumerate(group):
            print(f"{member}")
            # print(f"Member ID is: {member['user_id']}")
            # print(f"Member Alias is: {member['alias']}")
            if str(member['user_id']) == str(user_id):
                # print("User found")
                current = i
            else:
                group_ips.append(member['ip'])

        print(group_ips)
        alias = group[current]['alias']
        print(f"Alias is set to: {alias}")
        group.pop(current)

        print(f"\nIn Handle Message\nFetched data is now:")
        for i, member in enumerate(group):
            print(f"Index {i} is: {member}")


        # print("CM 49: Efter DB Insert")
        # print(user[0]['alias'])
        print("Before Frame Generation")
        frame = "1" + sep + alias + sep + str(group_id) + sep + payload + sep + str(time)
        print("After Frame Generation")
        # print("CM 51: Efter Frame-creation")
        packet = bytes(frame, 'utf-8')
        # print("CM 51: Efter Frame-2-bytes")
        print(f"Broadcast frame is: {packet}")
        self.broadcast(packet, conn, group_ips)


    """Using the below function, we broadcast the message to all
    clients who's object is not the same as the one sending
    the message """
    def broadcast(self, message, connection, group_ips):
        print("Inside Broadcast")
        print("Clients to send to: ")
        print(len(self.list_of_clients))
        print(f"Separator from Broadcast is: {sep}")


        for client in self.list_of_clients:		# For everyone in the chat
            current_ip = client.getpeername()[0]
            # print(current_ip)
            # if current_ip in group_ips:
            #     print("Den er der!... første gang")


            # if client != connection and current_ip in group_ips:			# Unless it's the sender themself
            if current_ip in group_ips:			# Unless it's the sender themself
                # dir(client)
                # print(f'Message sent to client {client}')
                try:
                    client.send(message)
                except:
                    print("Didn't send to client " + client)
                    client.close()

                    # if the link is broken, we remove the client
                    self.remove(client)


    def recv_and_sort(self, message, conn):
        packet = str(message.decode('utf8'))
        list = packet.split(sep)

        if list[0] == '0':
            user_id = list[1]
            group_id = list[2]
            payload = list[3]
            self.handle_incoming_msg(conn, user_id, group_id, payload)

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
                        print("\nReceived message from client")
                        """prints the message and address of the
                        user who just sent the message on the server
                        terminal"""
                        print ("<" + addr[0] + "> " + message.decode('utf-8'))

                        # packet= str(message.decode('utf-8'))
                        # list = packet.split(sep)

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
    #################################
    #  -- Argument Parsing Setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, required=False)
    parser.add_argument('-port', type=int, required=False)
    args = parser.parse_args()
    # takes the IP argument from command prompt as IP address, if any exists
    IP_address = str(args.ip) if args.ip else "127.0.0.1"

    # takes Port argument from command prompt as port number, if any exists
    Port = int(args.port) if args.port else 9000

    print(f"Readied IP is: {IP_address}")
    print(f"Readied Port is: {Port}")


    ###########################
    #  --  Main Program  -- 
    cm = ChatManager(IP_address, Port)
    cm.listener()
