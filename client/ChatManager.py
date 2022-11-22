import socket
from _thread import *

ClientMultiSocket = socket.socket()
#host = '127.0.0.1'
host = '192.168.1.105'
port = 2004
print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)

def send_to_server(connection):
    while True:
        Input = input('Hey there: ')
        connection.send(str.encode(Input))

def recv_from_server(connection):
    while True:
        res = connection.recv(1024)
        print(res.decode('utf-8'))

# while True:
#     Input = input('Hey there: ')
#     ClientMultiSocket.send(str.encode(Input))
#     res = ClientMultiSocket.recv(1024)
#     print(res.decode('utf-8'))
t1 = start_new_thread(send_to_server, (ClientMultiSocket, ))
t2 = start_new_thread(recv_from_server, (ClientMultiSocket, ))



ClientMultiSocket.close()
