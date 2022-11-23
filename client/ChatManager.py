# Python program to implement client side of chat room.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import socket
import select
import sys
import json
import User

class ChatManager:

    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if len(sys.argv) != 3:
            print ("Correct usage: script, IP address, port number")
            exit()
        self.IP_address = ip
        self.Port = port
        self.server.connect((self.IP_address, self.Port))

    def first_fetch(self):
        # get all group objects from database
        pass

    def handle_message(self, text, group_id):
        # send text to all users in the group with group_id
        pass

    def create_group(self):
        pass

    def join_group(self, invite_code):
        pass

    def leave_group(self, group_id):
        pass

    def encrypt_msg(self, msg_text, group_id):
        """Encrypt message with {group_id} secret key"""
        with open(".data.json", "r") as file:
            info = json.load(file)
            enc_key = info[f"{group_id}"]

        enc = Fernet(enc_key)
        msg_text = enc.encrypt(bytes(msg_text, 'utf-8'))
        return msg_text

    def decrypt_msg(self, cipher_text, group_id):
        """Decrypt message with {group_id} secret key"""
        with open(".data.json", "r") as file:
            info = json.load(file)
            enc_key = info[f'{group_id}']

        enc = Fernet(enc_key)
        msg_text = enc.decrypt(cipher_text) # Will throw error if cipher_text is not bytes
        return msg_text
        
    def authenticate(self, user):
        """Sign message for server-side user verification"""
        std_message = b'SuperHemmeligNisse'
        user_signature = user.private_key.sign(
            std_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Add communication to Server
    
    def store_key(self, group_id, key):
        """Store symmetric key for group locally """
        with open(".data.json", "r+") as file:
            info = json.load(file)
            info["Groups"].append(f"\"{group_id}\":\"{key}\"")
            json.dump(info, file)
    
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
                    message = bytes(sys.stdin.readline(), 'utf-8')
                    self.server.send(message)


        server.close()


if __name__ == "__main__":
    cm = ChatManager(str(sys.argv[1]), int(sys.argv[2]))
    cm.run()
