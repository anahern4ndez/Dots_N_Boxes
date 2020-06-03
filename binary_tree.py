from minimax import *
# class Node:
#     def __init__(self, value, board):
#         self.left = None
#         self.right = None
#         self.value = 99
#         self.movement = []
#         self.children = [self.left, self.right]
    
#     # def insert_children(self):
#     #     self.left = Node()
#     #     self.right = Node()

#     # def change_node_value(self, value):
#     #     self.value = value
    
#     # def set_value(self, value, state):
#     #     self.value = value
#     #     self.state = state

#     def fill(self, score, movement):
#         for node in self.children:
#             node.fill(score, movement)

#     def PrintNode(self):
#         if self.left:
#             self.left.PrintNode()
#         print(self.value),
#         if self.right:
#             self.right.PrintNode()

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
            self.children = []

    def fill(self, score, board, player, depth):
        for node in self.children:
            score, movement, new_board = value_node(board, not player)
            self.value = score
            self.movement = movement
            node.fill(score, new_board, not player, depth -1)
            if depth != 0:
                node.create_children(depth-1)
        return self.children

    def PrintNode(self, height):
        print(self.value)
        if height != 0:
            self.create_children(height-1)
            if self.children != None:
                for node in self.children:
                    node.PrintNode(height-1)

# class Tree:
#     def __init__(self, height):
#         self.nodes = []
#         self.height = height
#         self.nodes.append(Node()) # insert root node 
    
#     def fill_tree(self, level):
#         if level == self.height+1: return 
#         for node in self.nodes:
#             self.nodes.append(node)
#             node.insert_children()
#         self.fill_tree(level+1)
    
#     def print_tree(self):
#         self.nodes[0].PrintNode()

