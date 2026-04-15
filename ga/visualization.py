import io
import matplotlib.pyplot as plt


def create_route_figure(route, title: str = "Optimized Delivery Route"):
    x_coords = [city.x for city in route]
    y_coords = [city.y for city in route]

    x_coords.append(route[0].x)
    y_coords.append(route[0].y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_coords, y_coords, marker="o")

    for city in route:
        ax.text(city.x, city.y, f"{city.id}", fontsize=9)

    ax.set_title(title)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.grid(True)

    return fig


def create_convergence_figure(distance_history, title: str = "GA Convergence"):
    generations = list(range(1, len(distance_history) + 1))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(generations, distance_history)

    ax.set_title(title)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Distance")
    ax.grid(True)

    return fig


def figure_to_png_bytes(fig) -> bytes:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return buffer.getvalue()
