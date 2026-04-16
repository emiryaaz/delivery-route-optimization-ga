import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from ga.utils import generate_cities, find_best_random_route
from ga.solver import GeneticTSPSolver
from ga.visualization import (
    create_route_figure,
    create_convergence_figure,
    figure_to_png_bytes
)

def save_experiment_dataframe(result_df, experiment_type):
    os.makedirs("outputs", exist_ok=True)

    if experiment_type == "Population Size":
        output_path = "outputs/population_experiment_results.csv"
    elif experiment_type == "Mutation Rate":
        output_path = "outputs/mutation_experiment_results.csv"
    else:
        output_path = "outputs/generation_experiment_results.csv"

    result_df.to_csv(output_path, index=False)
    return output_path

def summarize_results(distances):
    average_distance = sum(distances) / len(distances)
    best_distance = min(distances)
    worst_distance = max(distances)
    return average_distance, best_distance, worst_distance


def run_experiment(
    experiment_type,
    parameter_values,
    num_cities,
    city_seed,
    population_size,
    generations,
    mutation_rate,
    elitism_count,
    tournament_size,
    runs_per_setting
):
    cities = generate_cities(num_cities=num_cities, seed=city_seed)
    results = []

    progress_bar = st.progress(0)
    total_runs = len(parameter_values) * runs_per_setting
    completed_runs = 0

    for parameter_value in parameter_values:
        distances = []

        for run in range(runs_per_setting):
            current_population_size = population_size
            current_mutation_rate = mutation_rate
            current_generations = generations

            if experiment_type == "Population Size":
                current_population_size = int(parameter_value)
            elif experiment_type == "Mutation Rate":
                current_mutation_rate = float(parameter_value)
            elif experiment_type == "Generation Count":
                current_generations = int(parameter_value)

            solver = GeneticTSPSolver(
                cities=cities,
                population_size=current_population_size,
                generations=current_generations,
                mutation_rate=current_mutation_rate,
                elitism_count=elitism_count,
                tournament_size=tournament_size,
                seed=1000 + run,
                verbose=False
            )

            _, best_distance = solver.evolve()
            distances.append(best_distance)

            completed_runs += 1
            progress_bar.progress(completed_runs / total_runs)

        average_distance, best_distance, worst_distance = summarize_results(distances)

        row = {
            "parameter_value": parameter_value,
            "run_1": distances[0] if len(distances) > 0 else None,
            "run_2": distances[1] if len(distances) > 1 else None,
            "run_3": distances[2] if len(distances) > 2 else None,
            "run_4": distances[3] if len(distances) > 3 else None,
            "run_5": distances[4] if len(distances) > 4 else None,
            "average_best_distance": average_distance,
            "best_of_runs": best_distance,
            "worst_of_runs": worst_distance,
        }
        results.append(row)

    progress_bar.empty()
    return pd.DataFrame(results)

st.set_page_config(page_title="Delivery Route Optimization GA", layout="wide")

st.title("Delivery Route Optimization Using Genetic Algorithms")
st.write(
    "This application solves a single-vehicle delivery route optimization problem "
    "modeled as the Traveling Salesman Problem (TSP) using a Genetic Algorithm."
)

tab1, tab2, tab3 = st.tabs(["Optimization", "Experiment Results","Run Experiments"])

with tab1:
    st.sidebar.header("Algorithm Parameters")

    num_cities = st.sidebar.slider("Number of Cities", min_value=5, max_value=50, value=15, step=1)
    population_size = st.sidebar.slider("Population Size", min_value=10, max_value=300, value=100, step=10)
    generations = st.sidebar.slider("Number of Generations", min_value=10, max_value=500, value=200, step=10)
    mutation_rate = st.sidebar.slider("Mutation Rate", min_value=0.001, max_value=0.2, value=0.02, step=0.001)
    elitism_count = st.sidebar.slider("Elitism Count", min_value=1, max_value=10, value=2, step=1)
    tournament_size = st.sidebar.slider("Tournament Size", min_value=2, max_value=10, value=4, step=1)
    random_seed = st.sidebar.number_input("Random Seed", min_value=0, value=42, step=1)
    random_trials = st.sidebar.slider("Random Search Trials", min_value=100, max_value=5000, value=1000, step=100)

    run_button = st.sidebar.button("Run Optimization", use_container_width=True)

    if elitism_count >= population_size:
        st.error("Elitism count must be smaller than population size.")
    elif tournament_size > population_size:
        st.error("Tournament size cannot be greater than population size.")
    elif run_button:
        with st.spinner("Running optimization..."):
            cities = generate_cities(num_cities=num_cities, seed=random_seed)

            random_best_route, random_best_distance = find_best_random_route(
                cities,
                num_trials=random_trials
            )

            solver = GeneticTSPSolver(
                cities=cities,
                population_size=population_size,
                generations=generations,
                mutation_rate=mutation_rate,
                elitism_count=elitism_count,
                tournament_size=tournament_size,
                seed=random_seed,
                verbose=False
            )

            ga_best_route, ga_best_distance = solver.evolve()

            improvement = ((random_best_distance - ga_best_distance) / random_best_distance) * 100

            route_fig = create_route_figure(ga_best_route, title="Best Route Found by GA")
            convergence_fig = create_convergence_figure(
                solver.best_distance_history,
                title="GA Convergence Over Generations"
            )

            route_png = figure_to_png_bytes(route_fig)
            convergence_png = figure_to_png_bytes(convergence_fig)

        st.subheader("Results")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Random Search Best Distance", f"{random_best_distance:.2f}")
        metric_col2.metric("GA Best Distance", f"{ga_best_distance:.2f}")
        metric_col3.metric("Improvement", f"{improvement:.2f}%")

        graph_col1, graph_col2 = st.columns(2)

        with graph_col1:
            st.subheader("Optimized Route")
            st.pyplot(route_fig)
            st.download_button(
                label="Download Route Plot (PNG)",
                data=route_png,
                file_name="route_plot.png",
                mime="image/png",
                use_container_width=True
            )

        with graph_col2:
            st.subheader("Convergence Graph")
            st.pyplot(convergence_fig)
            st.download_button(
                label="Download Convergence Plot (PNG)",
                data=convergence_png,
                file_name="convergence_plot.png",
                mime="image/png",
                use_container_width=True
            )

        with st.expander("Best Route Order"):
            route_ids = [city.id for city in ga_best_route]
            route_ids.append(ga_best_route[0].id)
            st.write(" -> ".join(map(str, route_ids)))

        with st.expander("Parameter Summary"):
            st.write(f"Number of Cities: {num_cities}")
            st.write(f"Population Size: {population_size}")
            st.write(f"Generations: {generations}")
            st.write(f"Mutation Rate: {mutation_rate}")
            st.write(f"Elitism Count: {elitism_count}")
            st.write(f"Tournament Size: {tournament_size}")
            st.write(f"Random Seed: {random_seed}")
            st.write(f"Random Search Trials: {random_trials}")

        plt.close(route_fig)
        plt.close(convergence_fig)
    else:
        st.info("Set the parameters from the sidebar and click 'Run Optimization'.")

with tab2:
    st.subheader("Population Size Experiment Results")

    csv_path = "outputs/population_experiment_results.csv"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        st.write("The table below shows the results of repeated GA runs for different population sizes.")
        st.dataframe(df, use_container_width=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Experiment Results (CSV)",
            data=csv_bytes,
            file_name="population_experiment_results.csv",
            mime="text/csv",
            use_container_width=True
        )

        if "population_size" in df.columns and "average_best_distance" in df.columns:
            st.subheader("Average Best Distance by Population Size")
            chart_df = df[["population_size", "average_best_distance"]].set_index("population_size")
            st.line_chart(chart_df)
    else:
        st.warning(
            "Experiment results file not found. "
            "Run the experiment script first to generate outputs/population_experiment_results.csv."
        )

    st.divider()
    st.subheader("Generation Count Experiment Results")

    generation_csv_path = "outputs/generation_experiment_results.csv"

    if os.path.exists(generation_csv_path):
        generation_df = pd.read_csv(generation_csv_path)

        st.write("The table below shows the results of repeated GA runs for different generation counts.")
        st.dataframe(generation_df, use_container_width=True)

        generation_csv_bytes = generation_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Generation Experiment Results (CSV)",
            data=generation_csv_bytes,
            file_name="generation_experiment_results.csv",
            mime="text/csv",
            use_container_width=True
        )

        if "parameter_value" in generation_df.columns and "average_best_distance" in generation_df.columns:
            st.subheader("Average Best Distance by Generation Count")
            chart_df = generation_df[["parameter_value", "average_best_distance"]].rename(
                columns={"parameter_value": "generation_count"}
            ).set_index("generation_count")
            st.line_chart(chart_df)
    else:
        st.warning(
            "Generation experiment results file not found. "
            "Run the experiment from the Streamlit interface first."
        )

with tab3:
    st.subheader("Run Experiments Inside Streamlit")

    experiment_type = st.selectbox(
        "Experiment Type",
        ["Population Size", "Mutation Rate","Generation Count"]
    )

    col1, col2 = st.columns(2)

with col1:
    exp_num_cities = st.slider(
        "Number of Cities",
        min_value=5,
        max_value=50,
        value=15,
        step=1,
        key="exp_num_cities"
    )

    if experiment_type != "Generation Count":
        exp_generations = st.slider(
            "Generations",
            min_value=10,
            max_value=500,
            value=200,
            step=10,
            key="exp_generations"
        )
    else:
        exp_generations = 200

    exp_runs = st.slider(
        "Runs Per Setting",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        key="exp_runs"
    )

with col2:
    exp_city_seed = st.number_input(
        "City Seed",
        min_value=0,
        value=42,
        step=1,
        key="exp_city_seed"
    )

    if experiment_type == "Population Size":
        exp_mutation_rate = st.slider(
            "Base Mutation Rate",
            min_value=0.001,
            max_value=0.2,
            value=0.02,
            step=0.001,
            key="exp_mutation_rate"
        )
        exp_population_size = 100
        st.caption("Population size values will be taken from the list below.")

    elif experiment_type == "Mutation Rate":
        exp_population_size = st.slider(
            "Base Population Size",
            min_value=10,
            max_value=300,
            value=100,
            step=10,
            key="exp_population_size"
        )
        exp_mutation_rate = 0.02
        st.caption("Mutation rate values will be taken from the list below.")

    elif experiment_type == "Generation Count":
        exp_population_size = st.slider(
            "Base Population Size",
            min_value=10,
            max_value=300,
            value=100,
            step=10,
            key="exp_population_size"
        )
        exp_mutation_rate = st.slider(
            "Base Mutation Rate",
            min_value=0.001,
            max_value=0.2,
            value=0.02,
            step=0.001,
            key="exp_mutation_rate"
        )
        st.caption("Generation values will be taken from the list below.")

    st.markdown("### Parameter Values to Test")

    if experiment_type == "Population Size":
        parameter_text = st.text_input(
            "Enter population sizes separated by commas",
            value="20,50,100,150,200"
        )
    elif experiment_type == "Mutation Rate":
        parameter_text = st.text_input(
            "Enter mutation rates separated by commas",
            value="0.005,0.01,0.02,0.05,0.1"
        )
    else:
        parameter_text= st.text_input(
            "Enter generation counts separated by commas",
            value="50,100,150,200,300"
        )

    run_experiment_button = st.button("Run Experiment", use_container_width=True)

    if run_experiment_button:
        try:
            if experiment_type == "Population Size":
                parameter_values = [int(x.strip()) for x in parameter_text.split(",") if x.strip()]
            elif experiment_type == "Mutation Rate":
                parameter_values = [float(x.strip()) for x in parameter_text.split(",") if x.strip()]
            else:
                parameter_values = [int(x.strip()) for x in parameter_text.split(",") if x.strip()]

            if not parameter_values:
                st.error("Please enter at least one parameter value.")
            else:
                with st.spinner("Running experiment..."):
                    result_df = run_experiment(
                        experiment_type=experiment_type,
                        parameter_values=parameter_values,
                        num_cities=exp_num_cities,
                        city_seed=exp_city_seed,
                        population_size=exp_population_size,
                        generations=exp_generations,
                        mutation_rate=exp_mutation_rate,
                        elitism_count=2,
                        tournament_size=4,
                        runs_per_setting=exp_runs
                    )

                saved_path = save_experiment_dataframe(result_df, experiment_type)
                st.success(f"Experiment completed and saved to {saved_path}")

                st.subheader("Experiment Table")
                st.dataframe(result_df, use_container_width=True)

                st.subheader("Average Best Distance Chart")
                chart_df = result_df[["parameter_value", "average_best_distance"]].set_index("parameter_value")
                st.line_chart(chart_df)

                csv_bytes = result_df.to_csv(index=False).encode("utf-8")
                if experiment_type == "Population Size":
                    filename = "population_experiment_streamlit.csv"
                elif experiment_type == "Mutation Rate":
                    filename = "mutation_experiment_streamlit.csv"
                else:
                    filename = "generation_experiment_streamlit.csv"
                st.download_button(
                    label="Download Results as CSV",
                    data=csv_bytes,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )

        except ValueError:
            st.error("Please enter valid numeric values separated by commas.")

