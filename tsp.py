import random

from matplotlib import pyplot as plt

from algorithms.hill_climbing import HillClimbing
from algorithms.random_search import RandomSearch
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.tabu_search import TabuSearch
from visualizations.plotter import ConvergencePlotter
from avg_history import average_history
from benchmark import benchmark

num_of_cities_input=int(input("Enter the number of cities: "))

cities = {
    f"City{i}": (
        random.randint(0,100),
        random.randint(0,100)
    )
    for i in range(num_of_cities_input)
}

class TSPProblem():
    def __init__(self, cities):
        self.cities=cities
    
    def random_solution(self):
        route=list(self.cities.keys())
        random.shuffle(route)
        return route
    
    def evaluate(self, route):
        total_distance=0
        num_of_cities=len(self.cities)
        for i in range(num_of_cities):
            current_city=route[i]
            next_city=route[(i+1)%num_of_cities]
            p1=self.cities[current_city]
            p2=self.cities[next_city]
            distance=((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
            total_distance+=distance
        return total_distance
    
    def neighbor(self, route):
        new_route=route.copy()
        i,j=random.sample(range(len(route)),2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

problem = TSPProblem(cities)

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

num_cities = len(cities)

plotter = ConvergencePlotter(
    f"results/tsp_{num_cities}cities"
)

plotter.save_convergence_plot(curves, f"convergence_{num_cities}cities")
plotter.save_convergence_csv(curves, f"convergence_{num_cities}cities")
plt.show()