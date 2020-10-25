import io
import socket
from PIL import Image

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

def send_message(conn,msg):
    msglen = len(msg)
    outmsg = '{:08d}'.format(msglen)+msg
    conn.sendall(outmsg.encode())

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

readhost = input('Enter host IP (leave empty for localhost): ')
if len(readhost) > 8:
    host = readhost
print('Waiting for connection')
try:
    print('Connecting to '+str(host))
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = receive_message(ClientSocket)
while True:
    try:
        Input = ""
        while len(Input) == 0:
            Input = input('Say Something: ')
        send_message(ClientSocket, Input)
        if Input == ('bye'):
            print('You have broken connection.')
            break
        elif Input.lower() == ('text previewer'):
            Input = input("Please specify the text's URL that you would like to preview:")
            send_message(ClientSocket, Input)
            preview = receive_message(ClientSocket)
            print(preview)
        elif Input.lower() == ('killserver'):
            break
        Response = receive_message(ClientSocket)
        if not Response:
            break
        print(Response)
    except ConnectionAbortedError as e:
        print('Connection aborted.')
        break
    except ConnectionResetError as e:
        print('Connection reset.')
        break

ClientSocket.close()