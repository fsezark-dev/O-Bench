# O-Bench

**O-Bench** is a modular, research-oriented framework for benchmarking and analyzing metaheuristic optimization algorithms on NP-hard combinatorial optimization problems. It provides a unified environment for evaluating algorithmic performance, convergence dynamics, runtime efficiency, robustness, and scalability across multiple problem domains.

---

## Algorithms Implemented

| Algorithm | Type | Key Characteristic |
|---|---|---|
| Random Search | Baseline | No memory, pure exploration |
| Hill Climbing | Local Search | Greedy, exploits neighborhood |
| Simulated Annealing | Local Search | Probabilistic escape from local optima |
| Genetic Algorithm | Population-based | Crossover-driven structural search |
| Tabu Search | Local Search | Memory-based neighborhood avoidance |

---

## Problem Domains

### Traveling Salesman Problem (TSP)
Find the shortest route visiting all cities exactly once and returning to the start. Cities are randomly generated on a 100×100 grid.

- **Representation:** Permutation of city labels
- **Neighbor:** Random 2-city swap
- **Evaluation:** Total Euclidean tour distance

### 0/1 Knapsack Problem
Maximize total value of selected items without exceeding a weight capacity.

- **Representation:** Binary vector (include/exclude per item)
- **Neighbor:** Single bit-flip
- **Evaluation:** Negative total value (penalty applied for overweight solutions)
- **Capacity:** 30% of total item weight

---

## Results

### TSP — 20 Cities

![TSP 20 Cities Convergence](results/tsp_20cities/convergence_20cities.png)

| Algorithm | Best | Mean | Std | Avg Runtime |
|---|---|---|---|---|
| Random Search | 632.93 | 715.22 | 40.21 | 0.0047s |
| Hill Climbing | 356.61 | 437.15 | 49.27 | 0.0036s |
| Simulated Annealing | 365.22 | 430.31 | 39.03 | 0.0051s |
| Genetic Algorithm | 361.00 | 388.94 | 27.85 | 1.2400s |
| Tabu Search | 356.61 | 363.50 | 12.23 | 0.1992s |

### TSP — 50 Cities

![TSP 50 Cities Convergence](results/tsp_50cities/convergence_50cities.png)

| Algorithm | Best | Mean | Std | Avg Runtime |
|---|---|---|---|---|
| Random Search | — | — | — | — |
| Hill Climbing | — | — | — | — |
| Simulated Annealing | — | — | — | — |
| Genetic Algorithm | — | — | — | — |
| Tabu Search | — | — | — | — |

> Fill in 50-city results after running benchmarks.

---

## Key Findings

- **Tabu Search** achieves the best solution quality and consistency at 20 cities (lowest std dev), thanks to its memory mechanism preventing revisitation of recent local optima.
- **Genetic Algorithm** produces competitive solution quality but runs ~250× slower than single-solution methods at small scales — the cost-benefit shifts at larger instances.
- **Simulated Annealing** requires an iteration budget proportional to problem size. With a fixed budget, it can underperform Hill Climbing despite theoretical superiority — a parameter sensitivity issue documented in this project.
- **SA cooling schedule** was made adaptive: initial temperature is estimated by sampling random neighbor deltas to achieve ~80% acceptance early on; cooling rate is computed to reach `T=1.0` by the final iteration.
- **Random Search** degrades sharply with scale, confirming the value of guided search strategies.

---

## Project Structure

```
O-Benchmarking/
│
├── algorithms/
│   ├── random_search.py
│   ├── hill_climbing.py
│   ├── simulated_annealing.py
│   ├── genetic_algorithm.py
│   └── tabu_search.py
│
├── problems/
│   ├── tsp.py
│   └── knapsack.py
│
├── visualizations/
│   └── plotter.py
│
├── results/
│   ├── tsp_20cities/
│   └── knapsack_100items/
│
├── benchmark.py
├── avg_history.py
└── README.md
```

---

## How to Run

**Install dependencies:**
```bash
pip install matplotlib pandas numpy
```

**Run TSP benchmark:**
```bash
python problems/tsp.py
# Enter number of cities when prompted (e.g. 20, 50, 100)
```

**Run Knapsack benchmark:**
```bash
python problems/knapsack.py
```

Results (convergence plot + CSV) are saved automatically to `results/`.

---

## Design Philosophy

Every algorithm implements a common interface via the problem class:

```python
problem.random_solution()   # generate initial solution
problem.evaluate(solution)  # return scalar score (lower = better)
problem.neighbor(solution)  # return perturbed solution
problem.crossover(p1, p2)   # combine two solutions (GA)
```

This makes adding new algorithms or problem domains straightforward — no changes to existing code required.

---

## Experimental Setup

- **Trials:** 30 independent runs per algorithm per problem instance
- **Convergence curves:** Averaged across all 30 trials
- **Statistics reported:** Best, Mean, Std Dev, Average Runtime per trial
- **TSP cities:** Randomly generated on a 100×100 integer grid
- **Knapsack:** 100 items, weights ∈ [1, 50], values ∈ [10, 100], capacity = 30% of total weight
