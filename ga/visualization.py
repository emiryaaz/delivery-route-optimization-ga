import os
import matplotlib.pyplot as plt


def plot_route(route, title: str = "Optimized Delivery Route", save_path: str | None = None, show: bool = False):
    x_coords = [city.x for city in route]
    y_coords = [city.y for city in route]

    x_coords.append(route[0].x)
    y_coords.append(route[0].y)

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, marker="o")

    for city in route:
        plt.text(city.x, city.y, f"{city.id}", fontsize=9)

    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Route plot saved to: {save_path}")

    if show:
        plt.show()

    plt.close()


def plot_convergence(distance_history, title: str = "GA Convergence", save_path: str | None = None, show: bool = False):
    generations = list(range(1, len(distance_history) + 1))

    plt.figure(figsize=(8, 6))
    plt.plot(generations, distance_history)

    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Best Distance")
    plt.grid(True)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Convergence plot saved to: {save_path}")

    if show:
        plt.show()

    plt.close()
