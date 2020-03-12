def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    return winner_of(state) is not None or is_full_board(state)


def utility_of(state):
    if winner_of(state) == 'X':
        return +1
    elif winner_of(state) == 'O':
        return -1
    else:
        return 0


def successors_of(state):
    successors = []
    open = 0
    # How many open spots there are
    for move in range(9):
        if state[move] == move:
            open += 1
    # Decides which player's turn it is
    if open % 2 == 1:
        player = 'X'  # X makes odd numbered moves
    else:
        player = 'O'
    # Creates a successor for each available move
    for move in range(9):
        if state[move] == move:  # Its a 0, 1, 2, etc.
            successor = state[:]  # Copy list
            successor[move] = player  # Place the player
            successors.append((move, successor))
    # print('Successor: ' + str(successors))
    return successors


def is_full_board(state):
    for i in range(9):
        if state[i] not in ['X', 'O']:
            return False
    return True


def winner_of(state):
    '''
    Returns 'X' if the first player won the game, 'O' if the second player won
    the game, or None if the game has not finished yet or if it is a tie.
    '''
    # Checks horizontally
    for c in [0, 3, 6]:
        if state[c + 0] == state[c + 1] and state[c + 0] == state[c + 2]:
            return state[c + 0]
    # Checks vertically
    for c in [0, 1, 2]:
        if state[c + 0] == state[c + 3] and state[c + 0] == state[c + 6]:
            return state[c+0]
    # Checks diagonally [\]
    if state[0] == state[4] and state[0] == state[8]:
        return state[4]
    # Checks diagonally [/]
    if state[2] == state[4] and state[2] == state[6]:
        return state[4]
    return None


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
