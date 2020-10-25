import os
import socket
from _thread import *

import jobs, factorio2
from io import BytesIO
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
killreceived = False

print('Getting host IP...')
# try:
#     import urllib.request
#     readhost = urllib.request.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4").read().decode('utf-8')
# except Exception as e:
#     print(str(e))
# else:
#     host = readhost
print('Host IP is '+str(host))

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, id):
    try:
        global killreceived
        thread_id = id
        connection.send(str.encode('Welcome to the Server\n'))
        while True:
            data = connection.recv(2048)
            decodedata = data.decode('utf-8')
            reply = 'Server Says: ' + decodedata
            print('Thread ' + str(thread_id) + ' says: ' + decodedata)
            if not data:
                break
            elif decodedata == 'Text Previewer':
                data = connection.recv(4096)
                url = data.decode('utf-8')
                try:
                    text = jobs.text_previewer(url)
                    connection.send(text.encode('ascii'))
                except Exception:
                    connection.sendall(str.encode("We're sorry, the URL you specified is invalid."))
            elif data[:10] == b"KILLSERVER":
                killreceived = True
            elif killreceived:
                reply = 'Server killed, goodbye.'
                connection.sendall(str.encode(reply))
                break
            connection.sendall(str.encode(reply))
        connection.close()
    except Exception as e:
        print("Client " + str(thread_id) + " has severed connection: "+str(e))

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

def threaded_killswitch(sock):
    while True:
        if killreceived:
            sock.close()
            break

start_new_thread(threaded_server,(ServerSocket,))
start_new_thread(threaded_killswitch,(ServerSocket,))

while True:
    if killreceived:
        break