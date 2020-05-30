
HOST = '3.12.129.126'  # Standard loopback interface address
# HOST = 'localhost'  # Standard loopback interface address
PORT = 4000        # Port to listen on (non-privileged ports are > 1023)
USERNAME = 'ana lucia hernandez'
TOURNAMENT_ID = 1

CURRENT_GAME_ID = -1
PLAYER_TURN_ID = -1
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
#     print(data)

import socketio
import random

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('signin', {
        'user_name': USERNAME,
        'tournament_id': TOURNAMENT_ID,
        'user_role': 'player'
    })

@sio.on('ready')
def play(data):
    print(data)
    CURRENT_GAME_ID = data['game_id']
    PLAYER_TURN_ID = data['player_turn_id']
    narray = random.randint(0,1)
    line = random.randint(0,29)
    print("Movement made:" + str(narray) + ", " + str(line))
    sio.emit('play', {
          'tournament_id': TOURNAMENT_ID,
          'player_turn_id': PLAYER_TURN_ID,
          'game_id': CURRENT_GAME_ID,
          'movement': [narray, line]
    })

@sio.on('finish')
def finish(data):
    print("\nTerminó el juego.")
    if (data['player_turn_id'] != data['winner_turn_id']): print('\t->>>>>> Perdiste :(')
    else: print('\t->>>>>> Ganaste :)\n')
    sio.emit('player_ready', {
        'tournament_id': TOURNAMENT_ID,
        'player_turn_id': data['player_turn_id'],
        'game_id': data['game_id']
    })


@sio.on('ok_signin')
def ok_signin():
    print('Successfully signed in!')

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://'+ HOST + ':'+ str(PORT))
sio.wait()
