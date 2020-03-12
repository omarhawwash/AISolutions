import random


p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''

    child = []
    for x in range (0, 3):
        if mother[x] == 1 or father[x] == 1:
            child.append(1)
        else:
            child.append(0)
    return tuple(child)


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    mutated = False # Boolean that's changed when we've mutated
    mutation = () # Make mutation tuple = 0
    for x in range (len(individual)):  # For random variable in X as long as the individual's bits (so 3)
        if random.randint(0,1) == 1 and mutated == False:  # Make a random int, and if it's equal to 1, and the child hasn't been mutated yet
            mutation = mutation + (1,)  # mutate child by adding 1 to it's random bit
            mutated = True  # Set mutated to be true, so we don't mutate this child again
        else:
            mutation = mutation + (individual[x],)  # Otherwise, set the mutation tuple to be itself + the bit of the individual at the given bit (x)

    return mutation  # Self-explanatoey


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.

    ordered_population = list(population)
    selected = []  # make empty array with the selected child in population
    total_fitness = 0
    to_selection = []

    for x in ordered_population:
        current_fitness = fitness_fn(x)  # set current fitness to be equal to the value x in
        # our ordered population array to the input var fitness_fn
        total_fitness = total_fitness + current_fitness  # total fitness is equal to whatever it was
        # PLUS the current fitness

        for i in range (current_fitness):  # for every number in current fitness
            to_selection.append(x)  # add it to the selection array

    selected = [to_selection[int(random.uniform(0, total_fitness))],to_selection[int(random.uniform(0, total_fitness))]]
    print("Selected mom & dad", selected)
    return selected


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    fitness = 0

    if individual[0] == 1:
        fitness = fitness + 4
    if individual[1] == 1:
        fitness = fitness + 2
    if individual[2] == 1:
        fitness = fitness + 1

    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    #initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()
