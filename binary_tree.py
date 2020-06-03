from minimax import value_node, is_game_over
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
        
        if not is_game_over(board):
            # print('fill\n', board)
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
            + '\n\t\tleft child value: ' + str(self.children[0].value) + '\tleft child mov: ' + str(self.children[0].movement)\
            + '\n\t\tright child value: ' + str(self.children[1].value) + '\tright child mov: ' + str(self.children[1].movement)