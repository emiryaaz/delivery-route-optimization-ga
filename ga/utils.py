import random
from ga.city import City


def generate_cities(num_cities: int, seed: int | None = None) -> list[City]:
    if seed is not None:
        random.seed(seed)

    cities = []
    for i in range(num_cities):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        cities.append(City(id=i, x=x, y=y))

    return cities


def calculate_route_distance(route: list[City]) -> float:
    total_distance = 0.0

    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        total_distance += current_city.distance_to(next_city)

    return total_distance


def create_random_route(cities: list[City]) -> list[City]:
    route = cities[:]
    random.shuffle(route)
    return route


def find_best_random_route(cities: list[City], num_trials: int) -> tuple[list[City], float]:
    best_route = None
    best_distance = float("inf")

    for _ in range(num_trials):
        route = create_random_route(cities)
        distance = calculate_route_distance(route)

        if distance < best_distance:
            best_distance = distance
            best_route = route[:]

    return best_route, best_distance
