# Delivery Route Optimization Using Genetic Algorithms

This project was developed for the Evolutionary Computing course. It focuses on solving a single-vehicle delivery route optimization problem modeled as the Traveling Salesman Problem (TSP) by using a Genetic Algorithm (GA).

The system allows users to generate delivery locations, run route optimization with configurable GA parameters, visualize the best route, observe convergence behavior over generations, and perform parameter-based experiments through a Streamlit interface.

## Project Objective

The main objective of this project is to minimize the total travel distance of a delivery route that:

- starts from a depot or an initial location,
- visits each delivery location exactly once,
- returns to the starting point.

Since this problem is computationally difficult for large instances, a Genetic Algorithm is used as a practical metaheuristic solution approach.

## Features

The project currently includes the following features:

- random city generation for route optimization scenarios,
- route distance calculation,
- random search baseline for comparison,
- Genetic Algorithm-based route optimization,
- tournament selection,
- ordered crossover,
- swap mutation,
- elitism-based generation update,
- best route visualization,
- convergence graph visualization,
- Streamlit-based user interface,
- experiment execution for parameter analysis,
- saving experiment results as CSV files,
- viewing saved experiment results inside the application.

## Technologies Used

- Python
- Streamlit
- Matplotlib
- Pandas

## Project Structure

```text
delivery-route-optimization-ga/
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── ga/
│   ├── __init__.py
│   ├── city.py
│   ├── utils.py
│   ├── population.py
│   ├── operators.py
│   ├── solver.py
│   └── visualization.py
│
├── experiments/
│   ├── __init__.py
│   └── experiment_runner.py
│
├── outputs/
│   ├── route.png
│   ├── convergence.png
│   ├── population_experiment_results.csv
│   ├── mutation_experiment_results.csv
│   └── generation_experiment_results.csv
│
├── data/
└── docs/

Genetic Algorithm Components

The project uses the following GA components:

Chromosome Representation: each chromosome represents a route as a permutation of cities.
Initial Population: randomly generated valid routes.
Fitness Function: inverse of total route distance.
Selection Method: tournament selection.
Crossover Operator: ordered crossover (OX).
Mutation Operator: swap mutation.
Elitism: best individuals are preserved between generations.

Installation

It is recommended to use a virtual environment.

1. Clone the repository

git clone <your-repository-url>
cd delivery-route-optimization-ga

2. Create a virtual environment

python3 -m venv .venv

3. Activate the virtual environment

On Linux/macOS:

source .venv/bin/activate

On Windows:

.venv\Scripts\activate

4. Install dependencies

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Running the Project
Run the command-line version
python main.py

This will run the optimization process and generate route/convergence outputs depending on the current configuration of the project files.

Run the Streamlit interface
streamlit run app.py

After running this command, Streamlit will provide a local URL that can be opened in a browser.

Streamlit Application

The Streamlit application includes multiple sections:

Optimization

This section allows the user to:

select the number of cities,
configure GA parameters,
run the optimization,
compare GA results with random search,
view the optimized route,
view the convergence graph,
download generated plots.
Saved Experiment Results

This section displays previously saved experiment results from the outputs/ folder, including:

population size experiment results,
mutation rate experiment results,
generation count experiment results.

Run Experiments

This section allows the user to run experiments directly from the interface. Current experiment types include:

Population Size
Mutation Rate
Generation Count

The results are shown in tabular form, visualized with charts, and can also be downloaded as CSV files.

Experimentation

The project supports parameter analysis for the following settings:

population size,
mutation rate,
generation count.

These experiments help analyze how different GA configurations affect solution quality.

Saved experiment results are written to the outputs/ directory as CSV files.

Example Output

The project can produce the following outputs:

optimized delivery route plot,
convergence plot showing best distance across generations,
CSV files containing experiment results.

Notes
The current implementation focuses on a single-vehicle routing problem modeled as TSP.
Delivery locations are currently generated as 2D coordinates.
The project is designed to be extendable for more realistic logistics scenarios in future versions.
Possible Future Improvements

Possible extensions of the project include:

using real map-based coordinates,
integrating real road distance matrices,
supporting multiple vehicles,
adding delivery constraints such as vehicle capacity or time windows,
comparing GA with additional heuristics or metaheuristics,
improving experiment tracking and statistical analysis.
