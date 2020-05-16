
import socket

HOST = '3.12.129.126'  # Standard loopback interface address
# HOST = 'localhost'  # Standard loopback interface address
PORT = 4000        # Port to listen on (non-privileged ports are > 1023)
USERNAME = 'ana lucia hernandez'
TOURNAMENT_ID = 1000

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
#     print(data)

import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('signin', {
        'user_name': USERNAME,
        'tournament_id': TOURNAMENT_ID,
        'user_role': 'player'
    })

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('signin', {
        'user_name': USERNAME,
        'tournament_id': TOURNAMENT_ID,
        'user_role': 'player'
    })

@sio.on('ok_signin')
def ok_signin():
    print('Successfully signed in!')

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://'+ HOST + ':'+ str(PORT))
sio.wait()