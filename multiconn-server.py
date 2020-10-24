import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
killreceived = False

print('Getting host IP...')
try:
    import urllib.request
    readhost = urllib.request.urlopen("http://169.254.169.254/latest/meta-data/public-ipv4").read()
except Exception as e:
    print(str(e))
else:
    host = readhost
print('Host IP is '+str(host))

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, id):
    global killreceived
    thread_id = id
    connection.send(str.encode('Welcome to the Server\n'))
    while True:
        data = connection.recv(2048)
        decodedata = data.decode('utf-8')
        reply = 'Server Says: ' + decodedata
        if not data:
            break
        if data[:10] == b"KILLSERVER":
            killreceived = True
        if killreceived:
            reply = 'Server killed, goodbye.'
            connection.sendall(str.encode(reply))
            break
        print('Thread ' + str(thread_id) + ' says: ' + decodedata)
        connection.sendall(str.encode(reply))
    connection.close()

def threaded_server(sock):
    ThreadCount = 0
    while True:
        Client, address = sock.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        start_new_thread(threaded_client, (Client, ThreadCount))
        if killreceived:
            print('Server killed.')
            break
    sock.close()

start_new_thread(threaded_server,(ServerSocket,))
while True:
    if killreceived:
        ServerSocket.close()
        break