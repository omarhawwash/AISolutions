class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0, size=2):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.SEARCHED = False
        self.XPOS = None
        self.YPOS = None
        self.TOTAL_CLEAN = 0
        self.SIZE = size
        self.DIRTY = True

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


    def setX(self, x):
        self.XPOS = x


    def setY(self, y):
        self.YPOS = y


    def setClean(self, num):
        self.TOTAL_CLEAN = num


'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []

    initial_node = Node(INITIAL_STATE)
    initial_node.XPOS = INITIAL_STATE[0]
    initial_node.YPOS = INITIAL_STATE[1]


    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = h1(fringe)
        if node.TOTAL_CLEAN == node.SIZE*node.SIZE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("Current state: ", node.STATE)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node):
    successors = []
    children = successor_new(node)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.XPOS = child[0]
        s.YPOS = child[1]
        s.TOTAL_CLEAN = child[2]
        if node.DIRTY:
            s.DIRTY = True
        else:
            s.DIRTY = False
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''
def INSERT(node, queue):
    #queue.insert(0, node)  # DFS
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


def h1(queue):
    bestValue = 99999
    best = None
    for node in queue:
        if calculateBest(node) < bestValue:
            bestValue = calculateBest(node)
            best = node
    queue.remove(best)
    return best


def calculateBest(node):
    value = (node.SIZE*node.SIZE)-node.TOTAL_CLEAN + node.DEPTH
    return value



#Set succesors in the format (num, num, num)
def successor_new(node):
    successorStates = []
    if node.XPOS != 0:
        successorStates.append([node.XPOS-1, node.YPOS, node.TOTAL_CLEAN])

    if node.XPOS != node.SIZE-1:
        successorStates.append([node.XPOS +1, node.YPOS, node.TOTAL_CLEAN])

    if node.YPOS != 0:
        successorStates.append([node.XPOS, node.YPOS -1, node.TOTAL_CLEAN])

    if node.YPOS != node.SIZE-1:
        successorStates.append([node.XPOS, node.YPOS +1, node.TOTAL_CLEAN])

    if node.DIRTY:
        successorStates.append([node.XPOS, node.YPOS, node.TOTAL_CLEAN +1])
    else:
        successorStates.append([node.XPOS, node.YPOS, node.TOTAL_CLEAN])

    return successorStates



'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']

# xPos, yPos and total cleaned. Total cleaned needs to be the
INITIAL_STATE = (0, 0, 0)
# Note: In this case, goal state is when vacuum goes back to location A and both A and B are clean
# Can also be: GOAL_STATE = ('B', 1, 1)

'''
Complete state space including loops back to current state
Note: with loops back to current state, the DFS can be stuck in an infinite loop,
so in that case BFS is used to find the path to the goal state
'''
#                  Current State - Actions:     ---LEFT---               ---SUCK---             ---RIGHT---
STATE_SPACE = {('A', 0, 0): [('A', 0, 0), ('A', 1, 0), ('B', 0, 0)],
               ('B', 0, 0): [('A', 0, 0), ('B', 0, 1), ('B', 0, 0)],
               ('A', 1, 0): [('A', 1, 0), ('A', 1, 0), ('B', 1, 0)],
               ('B', 0, 1): [('A', 0, 1), ('B', 0, 1), ('B', 0, 1)],
               ('B', 1, 0): [('A', 1, 0), ('B', 1, 1), ('B', 1, 0)],
               ('A', 0, 1): [('A', 0, 1), ('A', 1, 1), ('B', 0, 1)],
               ('A', 1, 1): [('A', 1, 1), ('A', 1, 1), ('B', 1, 1)],
               ('B', 1, 1): [('A', 1, 1), ('B', 1, 1), ('B', 1, 1)]
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
