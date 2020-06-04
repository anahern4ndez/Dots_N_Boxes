from minimax import value_node, is_game_over
# clase para definir nodos del árbol creado para minimax. 
class Node:
    def __init__(self):
        self.value = 99 # score resultante de un movimiento 
        self.movement = [] # movimiento que haría
        self.children = [] # node children

    # asignare nodos hijos a este nodo
    # height: altura máxima del árbol
    def create_children(self, height):
        if height != 0:
            left = Node()
            right = Node()
            self.children= [left, right]
        else:
            self.children = None

    # darles score y movement a los nodos basados en los valores del nodo root. 
    # board: board resultante del movimiento del nodo padre 
    # player: minimizing o maximizing player
    # depth: K lookahead
    def fill(self, board, player, depth):
        if not is_game_over(board):
            # crearle el valor y movement a los nodos hijos basados en este nodo
            # siempre que hayan posiciones disponibles 
            for node in self.children:
                if not is_game_over(board):
                    score, movement, new_board = value_node(board, player)
                    self.value = score
                    self.movement = movement
                    if depth > 0:
                        node.create_children(depth-1)
                    if node.children != None:
                        node.fill(new_board, not player, depth -1)
        return self.children

    # obtener valor de score del nodo
    def get_score(self):
        return self.value

    # setear valores de score y movement
    def set_move(self, score, movement):
        self.value = score
        self.movement = movement

    # imprimir árbol (debugging)
    def PrintNode(self):
        print(self.value)
        if self.children != None:
            for node in self.children:
                node.PrintNode()
    
    # obtener información del nodo (debugging)
    def toString(self):
        return '\tvalue: ' + str(self.value) + '\tmovement: ' + str(self.movement)\
            + '\n\t\tleft child value: ' + str(self.children[0].value) + '\tleft child mov: ' + str(self.children[0].movement)\
            + '\n\t\tright child value: ' + str(self.children[1].value) + '\tright child mov: ' + str(self.children[1].movement)