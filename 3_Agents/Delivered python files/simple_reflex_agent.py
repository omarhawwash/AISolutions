A = 'A'
B = 'B'

RULE_ACTION = {
    1: 'Suck'
}
rules = {
    (A, 'Dirty'): 1
}
# Ex. rule (if location == A && Dirty then rule 1)

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}


def INTERPRET_INPUT(input):  # No interpretation
    return input


def RULE_MATCH(state, rules):  # Match rule for a given state
    rule = rules.get(tuple(state))
    return rule


def SIMPLE_REFLEX_AGENT(percept):  # Determine action
    state = INTERPRET_INPUT(percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():  # Sense Environment
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):  # Modify Environment
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A


def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = SIMPLE_REFLEX_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(10)
