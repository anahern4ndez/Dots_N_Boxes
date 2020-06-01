
# HOST = '3.12.129.126'  # Standard loopback interface address
HOST = 'localhost'  # Standard loopback interface address
PORT = 4000        # Port to listen on (non-privileged ports are > 1023)
USERNAME = 'ana 2'
TOURNAMENT_ID = 1

CURRENT_GAME_ID = -1
PLAYER_TURN_ID = -1 # maximizer = 1; minimizer = 2

TREE_DEPTH = 5

import socketio
import random

# define si, para una config del board, todavia hay mas movimientos por hacer o no (game over)
def is_game_over(current_board):
    for array in current_board:
        for i in range(len(array)):
            if array[i] == 99:
                return False
    return True

# devuelve el movimiento que puede cerrar un box, si es posible
def can_close_box(current_board):
    for x in range(len(current_board)):
        other_array = 0 if x == 1 else 1
        print(other_array)
        # revisar si en el board hay 3 lineas que al agregarle la 4 cierra el box
        for k in range(len(current_board[x])):
            if (current_board[x][k+1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k+1] == 0) or \
                (current_board[x][k-1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k-1] == 0):
                return [x, k] # devuelve en cual array y en cual posicion del array puede hacer la linea para cerrar el cuadrado
    return None # devuelve none si no encuentra boxes para cerrar
# devuelve el board y score despues de hacer un movimiento
def make_movement(movement, current_board, player):
    score, a_boxes, b_boxes = 0,0,0 #score para el nodo, contador de boxes de player 1 y player 2 previos a un movimiento y posteriores 
    resulting_board = 0
    print(movement)
    array, position = movement
    current_board[array][position] = 0
    multiplier = 1 if player == 1 else -1
    # verificar si se cerro 1 box, 2, o ninguna
    # for x in range(len(current_board)):
    #     other_array = 0 if x == 1 else 1
    #     for k in range(len(current_board[x])):
    #         if k-5 < 0 or k-6 < 0 or k+5 > 29 or k+6 > 29:
    #             continue
    #         if (current_board[x][k+1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k+1] == 0 and \
    #             current_board[x][k-1] == 0 and current_board[other_array][k-6] == 0 and current_board[other_array][k-5] == 0) or \
    #             (current_board[x][k-1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k-1] == 0 and \
    #             ):
    other_array = 0 if array == 1 else 1
    # verificar si se cerro 1 o 2 boxes y llenar el board de acuerdo
    if position-5 < 0 or position-6 < 0 or position+5 > 29 or position+6 > 29:
        current_board[array][position] = 0
    elif (current_board[array][position+1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position+1] == 0 and \
        current_board[array][position-1] == 0 and current_board[other_array][position-6] == 0 and current_board[other_array][position-5] == 0) or \
        (current_board[array][position-1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position-1] == 0 and \
        current_board[array][position+1] == 0 and current_board[other_array][position+6] == 0 and current_board[other_array][position+5] == 0):
        current_board[array][position] = 2*multiplier
    elif (current_board[array][position+1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position+1] == 0) or \
        (current_board[array][position-1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position-1] == 0):
        current_board[array][position] = 1*multiplier

    # obtener el nuevo score tras el movimiento
    for array in current_board:
        for i in range(len(array)):
            if array[i] > 0: a_boxes += array[i]
            elif array[i] < 0: b_boxes += array[i]
    score = a_boxes - b_boxes
    return [score, movement]
    
def value_node(current_board, player):
    # score, a_boxes_pre, b_boxes_pre, a_boxes_post, b_boxes_post = 0,0,0,0,0 #score para el nodo, contador de boxes de player 1 y player 2 previos a un movimiento y posteriores 
    score, a_boxes, b_boxes = 0,0,0 #score para el nodo, contador de boxes de player 1 y player 2 previos a un movimiento y posteriores 
    available_positions = [] # se guardara los lugares en donde se puede hacer un movimiento
    # contar cuantos boxes se ha cerrado para cada player 
    for array in current_board:
        for i in range(len(array)):
            # if array[i] > 0: a_boxes_pre += array[i]
            # elif array[i] < 0: b_boxes_pre += array[i]
            # else: 
            available_positions.append([current_board.index(array), i])
    # print(a_boxes_pre, b_boxes_pre)
    # score = a_boxes_pre - b_boxes_pre
    # hacer un movimiento 
    movement = can_close_box(current_board)
    if movement == None:
        movement = available_positions[random.randint(0,len(available_positions)-1)]
    return make_movement(movement, current_board, player)

def minimax(position, depth, alpha, beta, maximizingPlayer):
    if is_game_over or depth == 0:
        return 


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
