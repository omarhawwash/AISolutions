def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for state in successors_of(state):
            v = max(v, min_value(state))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for state in successors_of(state):
            v = min(v, max_value(state))
        return v

    infinity = float('inf')
    state = argmax(successors_of(state), lambda a: min_value(a))
    return state


"""
Go over each pile in the state. If there is no pile that is larger than three. Then you lose
"""


def is_terminal(state):
    for pileSize in state:
        terminal = True
        if pileSize >= 3:
            terminal = False
    return terminal


"""
If the length of the state is divisible with two then the computer will have lost because the player made the last move.
Therefore you need to look for state with an uneven length of the piles.
"""


def utility_of(state):
    if len(state) % 2 == 0:
        return -1
    else:
        return 1


"""
Create a list of all possible successor states.
"""


def successors_of(state):
    possible_states = []

    # Go over every pile in the current state
    for pile in state:
        upper_range = int(pile/2)
        # If The pile is smaller than 3, then skip the pile
        if pile < 3:
            continue

        # Go over each possible split
        for j in range(1, upper_range):

            # Make a copy and remove the original pile from it.
            new_possible_states = state[:]
            new_possible_states.remove(pile)

            # If the pile is even numbered and the current number is the middle one, then skip because it is illegal
            if pile % 2 == 0 and j == pile / 2:
                continue

            # Add the two new piles to the state
            new_possible_states.append(j)
            new_possible_states.append(pile - j)
            possible_states.append(new_possible_states)

    return possible_states


def display(state):
    print(state)


def main():
    state = [15]
    while not is_terminal(state):
        state = minmax_decision(state)
        if not is_terminal(state):
            display(state)

            # Get user input for game.
            choice = int(input("Choose the pile that you want to split"))
            choice_two = int(input("Choose how many tokens you want in the first pile"))
            new_pile = state[choice-1] - choice_two

            # Check to see if the choice that was mad was legal
            if choice_two + new_pile < state[choice-1]:
                print("YOU MADE AN ILLEGAL MOVE! I AM ENDING THE GAME!!!")
                quit()

            # Remove old and add new piles to the state
            state.remove(state[choice-1])
            state.append(choice_two)
            state.append(new_pile)
            display(state)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
