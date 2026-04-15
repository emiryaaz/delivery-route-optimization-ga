import random

from ga.population import create_initial_population, rank_population
from ga.operators import tournament_selection, ordered_crossover, swap_mutation
from ga.utils import calculate_route_distance


class GeneticTSPSolver:
    def __init__(
        self,
        cities,
        population_size: int = 100,
        generations: int = 200,
        mutation_rate: float = 0.02,
        elitism_count: int = 2,
        tournament_size: int = 3,
        seed: int | None = None,
        verbose: bool = True
    ):
        self.cities = cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        self.seed = seed
        self.verbose = verbose

        self.best_route = None
        self.best_distance = float("inf")
        self.best_distance_history = []

    def create_next_generation(self, ranked_population):
        next_generation = []

        elites = ranked_population[:self.elitism_count]
        for route, _ in elites:
            next_generation.append(route[:])

        while len(next_generation) < self.population_size:
            parent1 = tournament_selection(ranked_population, self.tournament_size)
            parent2 = tournament_selection(ranked_population, self.tournament_size)

            max_attempts = 10
            attempt = 0
            while parent2 == parent1 and attempt < max_attempts:
                parent2 = tournament_selection(ranked_population, self.tournament_size)
                attempt += 1

            child = ordered_crossover(parent1, parent2)
            child = swap_mutation(child, self.mutation_rate)

            next_generation.append(child)

        return next_generation

    def evolve(self):
        if self.seed is not None:
            random.seed(self.seed)

        population = create_initial_population(self.cities, self.population_size)

        for generation in range(self.generations):
            ranked_population = rank_population(population)

            current_best_route = ranked_population[0][0]
            current_best_distance = calculate_route_distance(current_best_route)

            if current_best_distance < self.best_distance:
                self.best_distance = current_best_distance
                self.best_route = current_best_route[:]

            self.best_distance_history.append(self.best_distance)

            if self.verbose and ((generation + 1) % 10 == 0 or generation == 0):
                print(
                    f"Generation {generation + 1}/{self.generations} "
                    f"- Best Distance: {self.best_distance:.2f}"
                )

            population = self.create_next_generation(ranked_population)

        return self.best_route, self.best_distance
