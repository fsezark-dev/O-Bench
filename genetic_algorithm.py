import random


class GeneticAlgorithm:
    def __init__(self, population_size=50, generations=1000, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def tournament_selection(self, population, problem, k=3):
        candidates = random.sample(population, k)
        return min(
            candidates,
            key=problem.evaluate
        )

    def crossover(self, parent1, parent2, problem=None):
        if problem and hasattr(problem, 'cities'):
            size = len(parent1)
            start, end = sorted(random.sample(range(size), 2))
            child = [None] * size
            child[start:end] = parent1[start:end]
            pointer = 0
            for city in parent2:
                if city not in child:
                    while child[pointer] is not None:
                        pointer += 1
                    child[pointer] = city
            return child

        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    def mutate(self, child, problem):
        if random.random() < self.mutation_rate:
            return problem.neighbor(child)

        return child

    def solve(self, problem):

        population = [
            problem.random_solution()
            for _ in range(self.population_size)
        ]

        history = []

        best_solution = None
        best_score = float("inf")

        for _ in range(self.generations):

            population.sort(
                key=problem.evaluate
            )

            current_best = population[0]
            current_score = problem.evaluate(
                current_best
            )

            if current_score < best_score:
                best_solution = current_best.copy()
                best_score = current_score

            history.append(best_score)

            new_population = []

            # elitism
            new_population.append(
                population[0].copy()
            )

            while (
                len(new_population)
                < self.population_size
            ):

                parent1 = self.tournament_selection(
                    population,
                    problem
                )

                parent2 = self.tournament_selection(
                    population,
                    problem
                )

                child = self.crossover(parent1, parent2, problem)

                child = self.mutate(
                    child,
                    problem
                )

                new_population.append(child)

            population = new_population

        return (best_solution, best_score, history)