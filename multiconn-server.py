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

def send_message(conn,msg, encoding = 'utf-8'):
    msglen = len(msg)
    outmsg = '{:08d}'.format(msglen)+msg
    conn.sendall(outmsg.encode(encoding))

def receive_message(conn):
    msghdr = conn.recv(8)
    if not msghdr:
        return None
    msglen = int(msghdr.decode('utf-8'))
    inbuff = b''
    while msglen > 0:
        inbuff = inbuff + conn.recv(min(msglen,4096))
        msglen = msglen - min(msglen,4096)
    return inbuff.decode('utf-8')

def threaded_client(connection, id):
    try:
        global killreceived
        thread_id = id
        send_message(connection,'Welcome to the Server\n')
        while True:
            decodedata = receive_message(connection)
            reply = 'Server Says: ' + decodedata
            print('Thread ' + str(thread_id) + ' says: ' + decodedata)
            if not decodedata:
                break
            elif decodedata.lower() == 'factorio calculator':
                success = factorio2.runprogram(connection)
                if not success:
                    break
            elif decodedata.lower() == 'text previewer':
                url = receive_message(connection)
                try:
                    text = jobs.text_previewer(url)
                    send_message(connection,text,'ascii')
                except Exception:
                    send_message(connection, "We're sorry, the URL you specified is invalid.")
            elif decodedata.lower() == 'bye':
                pass
            elif decodedata[:10] == "KILLSERVER":
                killreceived = True
            if killreceived:
                reply = 'Server killed, goodbye.'
                send_message(connection, reply)
                break
            send_message(connection,reply)
        connection.close()
    except Exception as e:
        print('Client ' + str(thread_id) + ' has severed connection: '+str(e))

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
            sock.close()
            break

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