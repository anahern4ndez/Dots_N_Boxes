
# HOST = '3.12.129.126'  # Standard loopback interface address
HOST = '3.17.150.215'  # Standard loopback interface address
# HOST = 'localhost'  # Standard loopback interface address
# PORT = 4000        # Port to listen on (non-privileged ports are > 1023)
PORT = 9000
USERNAME = 'ana lucia'
TOURNAMENT_ID = 12

CURRENT_GAME_ID = -1
PLAYER_TURN_ID = -1 # maximizer = 1; minimizer = 2

TREE_DEPTH = 10
NEGATIVE_INF = float('-inf')
POSITIVE_INF = float('inf')

import socketio
import random
from minimax import *

class Node:
    def __init__(self):
        # left = None
        # right = None
        self.value = 99
        self.movement = []
        self.children = []

    def create_children(self, height):
        if height != 0:
            left = Node()
            right = Node()
            self.children= [left, right]
        else:
            self.children = None

    def fill(self, board, player, depth):
        for node in self.children:
            score, movement, new_board = value_node(board, player)
            self.value = score
            self.movement = movement
            if depth != 0:
                node.create_children(depth-1)
            if node.children != None:
                node.fill(new_board, not player, depth -1)
        return self.children

    def get_score(self):
        return self.value

    def set_move(self, score, movement):
        self.value = score
        self.movement = movement

    def PrintNode(self):
        print(self.value)
        # if height != 0:
        #     self.create_children(height-1)
        if self.children != None:
            for node in self.children:
                node.PrintNode()
    
    def toString(self):
        return '\tvalue: ' + str(self.value) + '\tmovement: ' + str(self.movement)\
            + '\n\t\tleft child value: ' + str(self.children[0].value) + '\n\t\tleft child mov: ' + str(self.children[0].movement)\
            + '\n\t\tright child value: ' + str(self.children[1].value) + '\n\t\tright child mov: ' + str(self.children[1].movement)

# state: current node
# depth: tree height (amount of look ahead)
# alpha: pruning limit for maximizing player
# beta:  pruning limit for minimizing player
# current_board: board of current state  
def minimax(state, depth, alpha, beta, maximizingPlayer, current_board):
    if is_game_over(current_board) or depth == 0:
        # print('state value: ', state.value)
        # print('state children: ', state.children)
        # print(state.toString())
        return state

    tree = state.fill(current_board, maximizingPlayer, depth+1)
    # print('tree')
    # print(tree)
    # print('maxplayer: ', maximizingPlayer)
    if maximizingPlayer:
        maxEval = NEGATIVE_INF
        for child in tree:
            evaluation = minimax(child, depth-1, alpha, beta, True, current_board)
            # print(evaluation.toString())
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
            # print(evaluation.toString())
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
    # narray = random.randint(0,1)
    # line = random.randint(0,29)
    maximizingPlayer = True if PLAYER_TURN_ID == 1 else False
    root = Node()
    root.create_children(TREE_DEPTH)
    alg = minimax(root, TREE_DEPTH +1 , NEGATIVE_INF, POSITIVE_INF, maximizingPlayer, data['board'])
    # print('return minimax: ', alg)
    movement = alg.__dict__['movement']
    print("Movement made:" + str(movement[0]) + ", " + str(movement[1]))
    sio.emit('play', {
          'tournament_id': TOURNAMENT_ID,
          'player_turn_id': PLAYER_TURN_ID,
          'game_id': CURRENT_GAME_ID,
          'movement': [movement[0], movement[1]]
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

# sio.connect('http://'+ HOST + ':'+ str(PORT))
sio.connect('http://876e10de0c24.ngrok.io')
sio.wait()
