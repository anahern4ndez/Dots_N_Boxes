import random

# devuelve una lista de todas las posiciones disponibles que hay en el board
def get_available_positions(current_board):
    available_positions = []
    for array in current_board:
        for i in range(len(array)):
            if array[i] == 99:
                available_positions.append([current_board.index(array), i])
    return available_positions

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
        # revisar si en el board hay 3 lineas que al agregarle la 4 cierra el box
        for k in range(len(current_board[x])):
            try:
                if ((current_board[x][k+1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k+1] == 0) or \
                    (current_board[x][k-1] == 0 and current_board[other_array][k] == 0 and current_board[other_array][k-1] == 0)) and \
                    current_board[x][k] == 99:
                    return [x, k] # devuelve en cual array y en cual posicion del array puede hacer la linea para cerrar el cuadrado
            except IndexError:
                continue
    return None # devuelve none si no encuentra boxes para cerrar

# devuelve el board y score despues de hacer un movimiento
def make_movement(movement, current_board, player):
    score, a_boxes, b_boxes = 0,0,0 #score para el nodo, contador de boxes de player 1 y player 2 previos a un movimiento y posteriores 
    array, position = movement
    current_board[array][position] = 0
    multiplier = 1 if player == 1 else -1 # para establecer el valor del board dependiendo al player
    other_array = 0 if array == 1 else 1
    # verificar si se cerro 1 o 2 boxes y llenar el board de acuerdo
    if position-5 < 0 or position-6 < 0 or position+5 > 29 or position+6 > 29:
        current_board[array][position] = 0
    # revisar si, al agregar la línea que cierra el box, se han cerrado dos boxes simultáneamente o solo una.
    # establece el valor del tablero de acuerdo al tipo de jugador y de cuántas boxes cerró en un movimiento 
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
    return [score, movement, current_board] # devolver el punteo que tendría si el movimiento se le realizara al board en ese momento

# método para determinar el score de un movimiento para un board determinado,
# para guardar esta información en uno de los nodos del árbol para minimax.  
def value_node(current_board, player):
    available_positions = [] # se guardara los lugares en donde se puede hacer un movimiento
    # obtener posiciones disponibles para dibujar linea
    available_positions = get_available_positions(current_board)
    movement = can_close_box(current_board)
    # si no puede cerrar un cuadro, escoger hacer una línea arbitraria. 
    if movement == None:
        movement = available_positions[random.randint(0,len(available_positions)-1)]
    return make_movement(movement, current_board, player)
