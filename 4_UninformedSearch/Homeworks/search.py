class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''
def INSERT(node, queue):
    queue.append(node)      # BFS
    return queue


'''
Insert list of nodes into the fringe
'''
def INSERT_ALL(list, queue):
    for node in list:
        INSERT(node, queue)
    return queue


'''
Remove first element from fringe
'''
def REMOVE_FIRST(queue):
    if len(queue) != 0:
        return queue.pop(0)
    return []

'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    states = STATE_SPACE[state]
    for stat in states:
        if stat == ('W', 'E', 'E', 'W'):
            states.remove(('W', 'E', 'E', 'W'))
        if stat == ('W', 'W', 'E', 'E'):
            states.remove(('W', 'W', 'E', 'E'))
        if stat == ('E', 'E', 'W', 'W'):
            states.remove(('E', 'E', 'W', 'W'))
        if stat == ('E', 'W', 'W', 'E'):
            states.remove(('E', 'W', 'W', 'E'))
    return states  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = ('W', 'W', 'W', 'W')
GOAL_STATE = ('E', 'E', 'E', 'E')

#             Current State - Actions:     ---LEFT---               ---SUCK---             ---RIGHT---
STATE_SPACE = {
                ('W', 'W', 'W', 'W'): [('E', 'E', 'W', 'W'), ('E', 'W', 'E', 'W'), ('E', 'W', 'W', 'E')],
                ('E', 'E', 'W', 'W'): [('W', 'E', 'W', 'W'), ('W', 'W', 'W', 'W')],
                ('E', 'W', 'E', 'W'): [('W', 'W', 'E', 'W'), ('W', 'W', 'W', 'W')],
                ('E', 'W', 'W', 'E'): [('W', 'W', 'W', 'E'), ('W', 'W', 'W', 'W')],

                ('W', 'E', 'W', 'W'): [('E', 'E', 'E', 'W'), ('E', 'E', 'W', 'E')],

                ('E', 'E', 'E', 'W'): [('W', 'W', 'E', 'W'), ('W', 'E', 'W', 'W'), ('W', 'E', 'E', 'W')],
                ('E', 'E', 'W', 'E'): [('W', 'E', 'W', 'E'), ('W', 'E', 'W', 'W'), ('W', 'W', 'W', 'E')],

                ('W', 'W', 'E', 'W'): [('E', 'E', 'E', 'W'), ('E', 'W', 'E', 'E')],

                ('E', 'W', 'E', 'E'): [('W', 'W', 'W', 'E'), ('W', 'W', 'E', 'W'), ('W', 'W', 'E', 'E')],

                ('W', 'E', 'E', 'W'): [('E', 'E', 'E', 'E')],
                ('W', 'E', 'W', 'E'): [('E', 'E', 'E', 'E')],
                ('W', 'W', 'E', 'E'): [('E', 'E', 'E', 'E')],

                ('W', 'W', 'W', 'E'): [('E', 'E', 'W', 'E'), ('E', 'W', 'E', 'E')],

                }

ILLGEAL_STATES ={
    ('W', 'E', 'E', 'W'),
    ('W', 'W', 'E', 'E')
}


'''
Run tree search and display the nodes in the path to goal node
'''
def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
