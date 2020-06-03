
from binary_tree import *

# tree = Tree(5)
# tree.fill_tree(0)
# tree.print_tree()
depth = 3
root = Node()
root.create_children(depth)
root.PrintNode(depth)