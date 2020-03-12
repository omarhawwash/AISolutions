from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]

        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp():
    costa_rica, panama, colombia, venezuela, guyana, suriname, guyana_fr, brasil, uruguay, argentina, chile, bolivia, paraguay, peru, ecuador = 'Costa Rica', 'Panama', 'Colombia', 'Venezuela', 'Guyana', 'Suriname', 'Guyana Fr', 'Brasil', 'Uruguay', 'Argentina', 'Chile', 'Bolivia', 'Paraguay', 'Peru', 'Ecuador'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [costa_rica, panama, colombia, venezuela, guyana, suriname, guyana_fr, brasil, uruguay, argentina, chile, bolivia, paraguay, peru, ecuador]
    domains = {
        costa_rica: values[:],
        panama: values[:],
        colombia: values[:],
        venezuela: values[:],
        guyana: values[:],
        suriname: values[:],
        guyana_fr: values[:],
        brasil: values[:],
        uruguay: values[:],
        argentina: values[:],
        chile: values[:],
        bolivia: values[:],
        paraguay: values[:],
        peru: values[:],
        ecuador: values[:],
    }
    neighbours = {
        costa_rica: [panama],
        panama: [costa_rica, colombia],
        colombia: [panama, ecuador, peru, brasil, venezuela],
        venezuela: [colombia, guyana, brasil],
        guyana: [venezuela, brasil, suriname],
        suriname: [guyana, brasil, guyana_fr],
        guyana_fr: [suriname, brasil],
        brasil: [guyana_fr, suriname, guyana, venezuela, colombia, peru, bolivia, paraguay, argentina, uruguay],
        uruguay: [argentina, brasil],
        argentina: [uruguay, brasil, paraguay, bolivia, chile],
        chile: [argentina, bolivia, peru],
        bolivia: [chile, argentina, brasil, paraguay, peru],
        paraguay: [argentina, brasil, bolivia],
        peru: [chile, bolivia, brasil, colombia, ecuador],
        ecuador: [peru, colombia],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        costa_rica: constraint_function,
        panama: constraint_function,
        colombia: constraint_function,
        guyana: constraint_function,
        suriname: constraint_function,
        guyana_fr: constraint_function,
        brasil: constraint_function,
        uruguay: constraint_function,
        argentina: constraint_function,
        chile: constraint_function,
        bolivia: constraint_function,
        paraguay: constraint_function,
        peru: constraint_function,
        ecuador: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
