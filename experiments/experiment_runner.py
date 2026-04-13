from ga.utils import generate_cities, find_best_random_route
from ga.solver import GeneticTSPSolver


def summarize_results(distances):
    average_distance = sum(distances) / len(distances)
    best_distance = min(distances)
    worst_distance = max(distances)

    return average_distance, best_distance, worst_distance


def run_population_size_experiment():
    num_cities = 15
    city_seed = 42
    generations = 200
    mutation_rate = 0.02
    elitism_count = 2
    tournament_size = 4

    population_sizes = [20, 50, 100, 150, 200]
    runs_per_setting = 5

    cities = generate_cities(num_cities=num_cities, seed=city_seed)

    print("=== Random Search Baseline ===")
    _, baseline_distance = find_best_random_route(cities, num_trials=1000)
    print(f"Random Search Best Distance: {baseline_distance:.2f}\n")

    print("=== Population Size Experiment ===")

    for population_size in population_sizes:
        distances = []

        print(f"\nTesting population_size = {population_size}")

        for run in range(runs_per_setting):
            solver = GeneticTSPSolver(
                cities=cities,
                population_size=population_size,
                generations=generations,
                mutation_rate=mutation_rate,
                elitism_count=elitism_count,
                tournament_size=tournament_size,
                seed=100 + run
            )

            _, best_distance = solver.evolve()
            distances.append(best_distance)

            print(f"  Run {run + 1}: Best Distance = {best_distance:.2f}")

        average_distance, best_distance, worst_distance = summarize_results(distances)

        print(f"  Average Best Distance: {average_distance:.2f}")
        print(f"  Best of Runs: {best_distance:.2f}")
        print(f"  Worst of Runs: {worst_distance:.2f}")


if __name__ == "__main__":
    run_population_size_experiment()
