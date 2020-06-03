

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
        # print(other_array)
        # revisar si en el board hay 3 lineas que al agregarle la 4 cierra el box
        for k in range(len(current_board[x])):
            try:
                # print(current_board[x][k+1])
                # print(current_board[other_array][k])
                # print(current_board[other_array][k+1])
                # print(current_board[x][k-1])
                # print(current_board[other_array][k])
                # print(current_board[other_array][k-1])
                # print(current_board[x][k])
                if ((current_board[x][k+1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k+1] == 0) or \
                    (current_board[x][k-1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k-1] == 0)) and \
                    current_board[x][k] == 99:
                    # print(x, k, current_board[x][k])
                    return [x, k] # devuelve en cual array y en cual posicion del array puede hacer la linea para cerrar el cuadrado
            except IndexError:
                continue
    return None # devuelve none si no encuentra boxes para cerrar
# devuelve el board y score despues de hacer un movimiento
def make_movement(movement, current_board, player):
    score, a_boxes, b_boxes = 0,0,0 #score para el nodo, contador de boxes de player 1 y player 2 previos a un movimiento y posteriores 
    array, position = movement
    current_board[array][position] = 0
    multiplier = 1 if player == 1 else -1
    other_array = 0 if array == 1 else 1
    # verificar si se cerro 1 o 2 boxes y llenar el board de acuerdo
    if position-5 < 0 or position-6 < 0 or position+5 > 29 or position+6 > 29:
        current_board[array][position] = 0
    elif ((current_board[array][position+1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position+1] == 0 and \
        current_board[array][position-1] == 0 and current_board[other_array][position-6] == 0 and current_board[other_array][position-5] == 0) or \
        (current_board[array][position-1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position-1] == 0 and \
        current_board[array][position+1] == 0 and current_board[other_array][position+6] == 0 and current_board[other_array][position+5] == 0)) and current_board[array][position] == 99:
        current_board[array][position] = 2*multiplier
    elif ((current_board[array][position+1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position+1] == 0) or \
        (current_board[array][position-1] == 0 and current_board[other_array][position] == 0 and current_board[other_array][position-1] == 0)) and current_board[array][position] == 99:
        current_board[array][position] = 1*multiplier

    # obtener el nuevo score tras el movimiento
    for array in current_board:
        for i in range(len(array)):
            if array[i] > 0 and array[i] < 99: a_boxes += array[i]
            elif array[i] < 0 and array[i] < 99: b_boxes += array[i]
    score = a_boxes - b_boxes
    return [score, movement, current_board]

def value_node(current_board, player):
    available_positions = [] # se guardara los lugares en donde se puede hacer un movimiento
    # obtener posiciones disponibles para dibujar linea
    for array in current_board:
        for i in range(len(array)):
            available_positions.append([current_board.index(array), i])
    # hacer un movimiento 
    movement = can_close_box(current_board)
    if movement == None:
        movement = available_positions[random.randint(0,len(available_positions)-1)]
    return make_movement(movement, current_board, player)
