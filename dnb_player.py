
# HOST = '3.12.129.126'  # Standard loopback interface address ---- server samuel
HOST = 'localhost'  # Standard loopback interface address
PORT = 4000        # Port to listen on (non-privileged ports are > 1023)
USERNAME = input('username: ')
TOURNAMENT_ID = 4000

CURRENT_GAME_ID = -1
PLAYER_TURN_ID = -1 # maximizer = 1; minimizer = 2

# minimax constants
TREE_DEPTH = 10
NEGATIVE_INF = float('-inf')
POSITIVE_INF = float('inf')

import socketio
import random
from minimax import *
from binary_tree import *

# Método de algoritmo minimax con poda alfabeta y K look ahead
# state: current node
# depth: tree height (amount of look ahead)
# alpha: pruning limit for maximizing player
# beta:  pruning limit for minimizing player
# current_board: board of current state  
# pseudoalgoritmo obtenido de https://www.youtube.com/watch?v=l-hh51ncgDI
def minimax(state, depth, alpha, beta, maximizingPlayer, current_board):
    if is_game_over(current_board) or depth == 0 or len(state.__dict__['children']) == 0:
        return state

    tree = state.fill(current_board, maximizingPlayer, depth-1) # crear el árbol de nodos llenos con scores y movements
    if maximizingPlayer:
        maxEval = NEGATIVE_INF
        for child in tree:
            evaluation = minimax(child, depth-1, alpha, beta, True, current_board)
            maxEval = max(maxEval, evaluation.get_score())
            alpha = max(alpha, evaluation.get_score())
            if beta <= alpha:
                break
            child.set_move(maxEval, evaluation.__dict__['movement'])
            return child
    else:
        minEval = POSITIVE_INF
        for child in tree:
            evaluation = minimax(child, depth-1, alpha, beta, False, current_board)
            minEval = min(minEval, evaluation.get_score())
            beta = min(beta, evaluation.get_score())
            if beta <= alpha:
                break
            child.set_move(minEval, evaluation.__dict__['movement'])
            return child


# conexión y mensajería cliente-server
sio = socketio.Client()

@sio.event
def connect():
    print('Connection established')
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
    av_pos = get_available_positions(data['board'])
    movement = []
    if len(av_pos) == 1:
        movement = av_pos[0]
    else:
        maximizingPlayer = True if PLAYER_TURN_ID == 1 else False
        root = Node()
        root.create_children(TREE_DEPTH)
        alg = minimax(root, TREE_DEPTH, NEGATIVE_INF, POSITIVE_INF, maximizingPlayer, data['board'])
        movement = alg.__dict__['movement']

    print("Movement made: " + str(movement), '\n')
    sio.emit('play', {
          'tournament_id': TOURNAMENT_ID,
          'player_turn_id': PLAYER_TURN_ID,
          'game_id': CURRENT_GAME_ID,
          'movement': movement
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
    print('Disconnected from server')

sio.connect('http://'+ HOST + ':'+ str(PORT))
sio.wait()
