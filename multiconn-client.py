import io
import socket
from PIL import Image

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

readhost = input('Enter host IP (leave empty for localhost): ')
if len(readhost) > 8:
    host = readhost
print('Waiting for connection')
try:
    print('Connecting to '+str(host))
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    try:
        Input = ""
        while len(Input) == 0:
            Input = input('Say Something: ')
        ClientSocket.send(str.encode(Input))
        if Input == ('bye'):
            print('You have broken connection.')
            break
        elif Input.lower() == ('text previewer'):
            Input = input("Please specify the text's URL that you would like to preview:")
            ClientSocket.sendall(str.encode(Input))
            preview = ClientSocket.recv(2048)
            preview = preview.decode('utf-8')
            print(preview)
        elif Input.lower() == ('killserver'):
            break
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    except ConnectionAbortedError as e:
        print('Connection aborted.')
        break
    except ConnectionResetError as e:
        print('Connection reset.')
        break

ClientSocket.close()