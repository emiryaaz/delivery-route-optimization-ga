from ga.utils import create_random_route, calculate_route_distance


def create_initial_population(cities, population_size: int):
    population = []

    for _ in range(population_size):
        route = create_random_route(cities)
        population.append(route)

    return population


def route_fitness(route) -> float:
    distance = calculate_route_distance(route)
    return 1 / distance if distance > 0 else float("inf")


def rank_population(population):
    ranked = []

    for route in population:
        ranked.append((route, route_fitness(route)))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked
