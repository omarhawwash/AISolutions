import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        # [None, 3, 1, 3],
        # [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end] Columns: ["initial", "hot", "cold", "final"]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation] Columns: [0, 1, 2, 3]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    qf = big_n + 1

    # Observations
    obs = observations

    # Transitions
    tr = transitions

    # Emissions
    em = emissions

    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    forward = 100 * np.ones((big_n + 2, big_t + 1))

    for sts in inclusive_range(1, big_n):
        forward[sts, 1] = tr[0, sts] * em[sts, obs[1]]

        for t in inclusive_range(2, big_t):
            for sts in inclusive_range(1, big_n):
                sum = 0
                for sts_mark in inclusive_range(1, big_n):
                    sum += forward[sts_mark, t - 1] * tr[sts_mark, sts] * em[sts, obs[t]]
                forward[sts, t] = sum
        print(forward)
        print('')

    probability = 0

    for s in inclusive_range(1, big_n):
        probability += forward[s, big_t] * tr[s, qf]

    return probability


def compute_viterbi(states, observations, transitions, emissions):
    big_n = len(states) - 2

    # The first element is dummy, so we ignore it
    big_t = len(observations) - 1

    # The last state
    qf = big_n + 1

    # Observations
    obs = observations

    # Transitions
    tr = transitions

    # Emissions
    em = emissions

    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    viterbi = 100 * np.ones((big_n + 2, big_t + 1))

    # Must be of type int, otherwise it is tricky to use its elements to index
    # the states
    # Initialize to 100, so it's easy to see what elements were not overwritten
    # (0 could be a valid value)
    backpointers = 100 * np.ones((big_n + 2, big_t + 1), dtype=int)

    for sts in inclusive_range(1, big_n):
        viterbi[sts, 1] = tr[0, sts] * em[sts, obs[1]]
        backpointers[sts, 1] = 0

    for t in inclusive_range(2, big_t):
        for sts in inclusive_range(1, big_n):
            viterbis_list = []
            backpointers_list = []
            for sts_prime in inclusive_range(1, big_n):
                viterbis_list.append(viterbi[sts_prime, t-1] * tr[sts_prime, sts] * em[sts, obs[t]])
                backpointers_list.append(viterbi[sts_prime, t-1] * tr[sts_prime, sts])
            viterbi[sts, t] = max(viterbis_list)
            backpointers[sts, t] = argmax(backpointers_list) + 1

    qf_viterbi = []
    qf_backpointer = []
    for sts in inclusive_range(1, big_n):
        qf_viterbi.append(viterbi[sts, big_t] * tr[sts, qf])
        qf_backpointer.append(viterbi[sts, big_t] * tr[sts, qf])
    viterbi[qf, big_t] = max(qf_viterbi)
    backpointers[qf, big_t] = argmax(qf_backpointer) + 1

    backpointers = backpointers[1:, 1:]
    state_index = big_t - 1
    result = []
    for i in reversed(range(len(backpointers))):
        state_index = backpointers[i, state_index]
        result.append(states[state_index])

    return result


def argmax(sequence):
    return max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
