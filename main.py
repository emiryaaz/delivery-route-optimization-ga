from ga.utils import generate_cities, find_best_random_route
from ga.solver import GeneticTSPSolver
from ga.visualization import plot_route, plot_convergence


def print_cities(cities):
    print("Generated Cities:")
    for city in cities:
        print(f"City {city.id}: ({city.x:.2f}, {city.y:.2f})")


def print_route(route):
    print("\nRoute:")
    for city in route:
        print(f"City {city.id}", end=" -> ")
    print(f"City {route[0].id}")


def main():
    cities = generate_cities(num_cities=15, seed=42)

    print_cities(cities)

    random_best_route, random_best_distance = find_best_random_route(cities, num_trials=1000)

    print("\nBest Route Found by Random Search (1000 trials)")
    print_route(random_best_route)
    print(f"Random Search Best Distance: {random_best_distance:.2f}")

    solver = GeneticTSPSolver(
        cities=cities,
        population_size=100,
        generations=200,
        mutation_rate=0.02,
        elitism_count=2,
        tournament_size=4
    )

    ga_best_route, ga_best_distance = solver.evolve()

    print("\nBest Route Found by Genetic Algorithm")
    print_route(ga_best_route)
    print(f"GA Best Distance: {ga_best_distance:.2f}")

    plot_route(
        ga_best_route,
        title="Best Route Found by GA",
       	save_path="outputs/route.png",
    	show=False
    )

    plot_convergence(
    	solver.best_distance_history,
    	title="GA Convergence Over Generations",
    	save_path="outputs/convergence.png",
    	show=False
    )

if __name__ == "__main__":
    main()
