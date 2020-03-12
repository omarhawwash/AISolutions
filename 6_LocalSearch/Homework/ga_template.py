import random
import importlib

moduleName = input('queens_fitness:')
importlib.import_module(moduleName)

p_mutation = 0.2
num_of_generations = 30
maxpopulation = 8


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

def remove_weakest_children(population, fitness_fn):

    while (len(population) < maxpopulation):
        weakest_child = None
        worst_fitness = 99999

        for child in population:  # for each child in the population array
            current_fitness = fitness_fn(child)     # set the current fitness = fitness of this child
            if current_fitness < worst_fitness:     # if current fitness is less than worst_fitness
                weakest_child = child               # set this child to be the weakest child
                worst_fitness = current_fitness     # and set this fitness to be the worst fitness

        population.remove(weakest_child)                    # remove child from population bc it's weak

    return population                               # return updated population

# we've defined how to remove the weakest child
# now we'll define how to find the negative fitness
# by calculating the number of conflicting pairs
# (alternative fitness function)

def fitness_fn_negative(individual):

    n = len(individual)
    fitness = 0
    for column, row in enumerate(individual):       # we do this due to how queens works, like a chessboard
        contribution = 0        # set initial contribution

        # Horizontal work
        for other_column in range (column + 1, n)   # column + 1 bc Python starts with 0
            if individual[other_column] == row:
                contribution += 1

        # Diagonals

def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    child = []
    for x in range(0, 3):
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
    mutated = False
    mutation = ()
    for x in range(0, len(individual)):
        if random.randint(0, 1) == 1 and mutated == False:
            mutation = mutation + (1,)
            mutated = True
        else:
            mutation = mutation + (individual[x],)

    return mutation


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
    selected = []
    total_fitness = 0
    to_selection = []

    for x in ordered_population:
        current_fitness = fitness_fn(x)
        total_fitness = total_fitness + current_fitness

        for i in range(current_fitness):
            to_selection.append(x)

    selected = [to_selection[int(random.uniform(0, total_fitness))],to_selection[int(random.uniform(0, total_fitness))]]
    # print ("selected mom and dad ", selected)
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
        (5, 6, 3, 3, 5, 8, 6, 1),
        (8, 1, 6, 1, 8, 3, 2, 8),
        (1, 2, 3, 4, 7, 8, 5, 1),
        (1, 5, 3, 4, 4, 4, 3, 5)
    }
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()
