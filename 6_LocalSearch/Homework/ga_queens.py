import random
import importlib

moduleName = input('queens_fitness:')
importlib.import_module(moduleName)

p_mutation = 0.2
num_of_generations = 100

pop_max = 8


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

            remove_weakest_children(population, fitness_fn)

            new_population.add(child)

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

    while len(population) > pop_max:
        weakest_child = None
        worst_fitness = 999999

        for child in population:
            current_fitness = fitness_fn(child)
            if current_fitness < worst_fitness:
                weakest_child = child
                worst_fitness = current_fitness

        population.remove(weakest_child)

    return population


def fitness_fn_negative(individual):
    """
    Compute the number of conflicting pairs, negated.
    For a solution with 5 conflicting pairs the return value is -5, so it can
    be maximized to 0.
    """

    n = len(individual)
    fitness = 0
    for column, row in enumerate(individual):
        contribution = 0

        # Horizontal
        for other_column in range(column + 1, n):
            if individual[other_column] == row:
                contribution += 1

        # Diagonals
        for other_column in range(column + 1, n):
            row_a = row + (column - other_column)
            row_b = row - (column - other_column)
            if 0 <= row_a < n and individual[other_column] == row_a:
                contribution += 1
            if 0 <= row_b < n and individual[other_column] == row_b:
                contribution += 1

        fitness += contribution

    return - fitness


def fitness_fn_positive(state):
    """
    Compute the number of non-conflicting pairs.
    """

    def conflicted(state, row, col):
        for c in range(col):
            if conflict(row, col, state[c], c):
                return True

        return False

    def conflict(row1, col1, row2, col2):
        return (
            row1 == row2 or
            col1 == col2 or
            row1 - col1 == row2 - col2 or
            row1 + col1 == row2 + col2
        )

    fitness = 0
    for col in range(len(state)):
        for pair in range(1, col + 1):
            if not conflicted(state, state[pair], pair):
                fitness = fitness + 1
    return fitness


def reproduce(mother, father):

    father_first = round(random.uniform(0, 1))
    index = round(random.uniform(1, 7))
    child = None

    if father_first == 1:
        child = father[0:index] + mother[index:]
    else:
        child = mother[0:index] + father[index:]

    return tuple(child)


def mutate(individual):
    individual_list = list(individual)

    s_mutate = random.randint(0, 100) < 50

    if s_mutate:
        random_index = random.randint(0, 7)
        random_number = random.randint(1, 8)
        individual_list[random_index] = random_number

    return tuple(individual_list)


def random_selection(population, fitness_fn_positive):

    total_fitness = 0

    roulette = []
    selected = []

    ordered_population = list(population)

    for i in range(0, len(ordered_population)):
        current_fitness = fitness_fn_positive(ordered_population[i])
        total_fitness += current_fitness
        if i == 0:
            roulette.append(current_fitness)
        else:
            a_fitness = roulette[i-1]
            roulette.append(current_fitness + a_fitness)

    first_selected_index = 0
    second_selected_index = 0

    first_random_fitness_selection = random.randint(0, total_fitness)
    second_random_fitness_selection = random.randint(0, total_fitness)

    for i in range(0, len(roulette)):
        if roulette[i] < first_random_fitness_selection < roulette[i + 1]:
            first_selected_index = i
        if roulette[i] < second_random_fitness_selection < roulette[i + 1]:
            second_selected_index = i

    for i in range(0, len(ordered_population)):
        if i == first_selected_index:
            selected.append(ordered_population[i])
        if i == second_selected_index:
            selected.append(ordered_population[i])
    print("SELECTED: ", selected)

    return selected


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    """
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    """
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    # 56 fields.
    minimal_fitness = 8*7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (5, 6, 3, 3, 5, 8, 6, 1),
        (8, 1, 6, 1, 8, 3, 2, 8),
        (1, 2, 3, 4, 7, 8, 5, 1),
        (1, 5, 3, 4, 4, 4, 3, 5)
    }

    fittest = genetic_algorithm(initial_population, fitness_fn_positive, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()
