import random

from matplotlib import pyplot as plt

from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.hill_climbing import HillClimbing
from algorithms.random_search import RandomSearch
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.tabu_search import TabuSearch
from avg_history import average_history
from benchmark import benchmark
from visualizations.plotter import ConvergencePlotter

NUM_ITEMS = 100

weights = [
    random.randint(1, 50)
    for _ in range(NUM_ITEMS)
]

values = [
    random.randint(10, 100)
    for _ in range(NUM_ITEMS)
]

capacity = int(sum(weights) * 0.3)

class KnapsackProblem:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity

    def random_solution(self):
        solution = [0] * len(self.weights)
        indices = list(range(len(self.weights)))
        random.shuffle(indices)
        total_weight = 0
        for i in indices:
            if total_weight + self.weights[i] <= self.capacity:
                solution[i] = 1
                total_weight += self.weights[i]
        return solution
    
    def evaluate(self, solution):
        total_weight = 0
        total_value = 0

        for i in range(len(solution)):
            if solution[i]:
                total_weight += self.weights[i]
                total_value += self.values[i]

        if total_weight > self.capacity:
            penalty = (total_weight - self.capacity) * max(self.values)
            score = -total_value + penalty
            return score

        return -total_value
    
    def neighbor(self, solution):
        new_solution = solution.copy()
        idx = random.randint(0, len(solution) - 1)
        new_solution[idx] = 1 - new_solution[idx]
        return new_solution
    
    def crossover(self, parent1, parent2):
        point = random.randint(
            1,
            len(parent1)-1
        )

        child = (
            parent1[:point]
            + parent2[point:]
        )

        return child
    def mutate(self, solution):

        idx = random.randint(
            0,
            len(solution)-1
        )

        solution[idx] = (
            1 - solution[idx]
        )

        return solution

problem = KnapsackProblem(weights, values, capacity)

rs_results = benchmark(
    RandomSearch(1000),
    problem,
    trials=30
)

hc_results = benchmark(
    HillClimbing(1000),
    problem,
    trials=30
)

sa_results = benchmark(
    SimulatedAnnealing(1000),
    problem,
    trials=30
)

ga_results = benchmark(
    GeneticAlgorithm(
        population_size=50,
        generations=1000,
        mutation_rate=0.1
    ),
    problem,
    trials=30
)

tabu_results = benchmark(
    TabuSearch(1000),
    problem,
    trials=30
)

print("===== RANDOM SEARCH =====")
print(
    f"Best={rs_results['best']:.2f} "
    f"Mean={rs_results['mean']:.2f} "
    f"Std={rs_results['std']:.2f} "
    f"Runtime={rs_results['runtime']:.4f}s"
)

print()

print("===== HILL CLIMBING =====")
print(
    f"Best={hc_results['best']:.2f} "
    f"Mean={hc_results['mean']:.2f} "
    f"Std={hc_results['std']:.2f} "
    f"Runtime={hc_results['runtime']:.4f}s"
)

print()

print("===== SIMULATED ANNEALING =====")
print(
    f"Best={sa_results['best']:.2f} "
    f"Mean={sa_results['mean']:.2f} "
    f"Std={sa_results['std']:.2f} "
    f"Runtime={sa_results['runtime']:.4f}s"
)

print()

print("===== GENETIC ALGORITHM =====")
print(
    f"Best={ga_results['best']:.2f} "
    f"Mean={ga_results['mean']:.2f} "
    f"Std={ga_results['std']:.2f} "
    f"Runtime={ga_results['runtime']:.4f}s"
)

print()

print("===== TABU SEARCH =====")
print(
    f"Best={tabu_results['best']:.2f} "
    f"Mean={tabu_results['mean']:.2f} "
    f"Std={tabu_results['std']:.2f} "
    f"Runtime={tabu_results['runtime']:.4f}s"
)

rs_curve = average_history(rs_results["histories"])
hc_curve = average_history(hc_results["histories"])
sa_curve = average_history(sa_results["histories"])
ga_curve = average_history(ga_results["histories"])
tabu_curve = average_history(tabu_results["histories"])

curves = {
    "Random Search": rs_curve,
    "Hill Climbing": hc_curve,
    "Simulated Annealing": sa_curve,
    "Genetic Algorithm": ga_curve,
    "Tabu Search": tabu_curve
}

num_items = NUM_ITEMS

plotter = ConvergencePlotter(f"results/knapsack_{num_items}items")

plotter.save_convergence_plot(curves, f"convergence_{num_items}items", ylabel="Best Objective")
plotter.save_convergence_csv(curves, f"convergence_{num_items}items")

plt.show()