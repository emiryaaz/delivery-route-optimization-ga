import csv
import os

from ga.utils import generate_cities, find_best_random_route
from ga.solver import GeneticTSPSolver


def summarize_results(distances):
    average_distance = sum(distances) / len(distances)
    best_distance = min(distances)
    worst_distance = max(distances)
    return average_distance, best_distance, worst_distance


def save_results_to_csv(results, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "population_size",
                "run_1",
                "run_2",
                "run_3",
                "run_4",
                "run_5",
                "average_best_distance",
                "best_of_runs",
                "worst_of_runs",
            ],
        )
        writer.writeheader()
        writer.writerows(results)


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

    all_results = []

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
                seed=100 + run,
                verbose=False,
            )

            _, best_distance = solver.evolve()
            distances.append(best_distance)

            print(f"  Run {run + 1}: Best Distance = {best_distance:.2f}")

        average_distance, best_distance, worst_distance = summarize_results(distances)

        print(f"  Average Best Distance: {average_distance:.2f}")
        print(f"  Best of Runs: {best_distance:.2f}")
        print(f"  Worst of Runs: {worst_distance:.2f}")

        result_row = {
            "population_size": population_size,
            "run_1": distances[0],
            "run_2": distances[1],
            "run_3": distances[2],
            "run_4": distances[3],
            "run_5": distances[4],
            "average_best_distance": average_distance,
            "best_of_runs": best_distance,
            "worst_of_runs": worst_distance,
        }
        all_results.append(result_row)

    save_results_to_csv(all_results, "outputs/population_experiment_results.csv")
    print("\nResults saved to: outputs/population_experiment_results.csv")


if __name__ == "__main__":
    run_population_size_experiment()
