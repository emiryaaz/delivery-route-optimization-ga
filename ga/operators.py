import random


def tournament_selection(ranked_population, tournament_size: int = 3):
    selected = random.sample(ranked_population, tournament_size)
    selected.sort(key=lambda item: item[1], reverse=True)
    return selected[0][0]


def ordered_crossover(parent1, parent2):
    size = len(parent1)

    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size

    for i in range(start, end + 1):
        child[i] = parent1[i]

    parent2_remaining = []
    for city in parent2:
        if city not in child:
            parent2_remaining.append(city)

    remaining_index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = parent2_remaining[remaining_index]
            remaining_index += 1

    return child


def swap_mutation(route, mutation_rate: float = 0.02):
    mutated_route = route[:]

    for i in range(len(mutated_route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(mutated_route) - 1)
            mutated_route[i], mutated_route[j] = mutated_route[j], mutated_route[i]

    return mutated_route
