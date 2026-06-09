import math
import random
import numpy as np


class SimulatedAnnealing:
    def __init__(
        self,
        iterations=1000,
        initial_temperature=None,
        cooling_rate=None,
        target_acceptance=0.8,    
        final_temperature=1.0      
    ):
        self.iterations = iterations
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.target_acceptance = target_acceptance
        self.final_temperature = final_temperature

    def _estimate_initial_temperature(self, problem, n_samples=200):
        deltas = []
        sol = problem.random_solution()
        for _ in range(n_samples):
            neighbor = problem.neighbor(sol)
            delta = problem.evaluate(neighbor) - problem.evaluate(sol)
            if delta > 0:
                deltas.append(delta)
            sol = neighbor

        if not deltas:
            return 50 

        avg_delta = np.mean(deltas)
        return -avg_delta / math.log(self.target_acceptance)

    def _estimate_cooling_rate(self, initial_temperature):
        # T_final = T_initial * rate^iterations => rate = (T_final/T_initial)^(1/iterations)
        return (self.final_temperature / initial_temperature) ** (1 / self.iterations)

    def solve(self, problem):
        accepted_worse = 0
        accepted_better = 0
        history = []

        current = problem.random_solution()
        current_score = problem.evaluate(current)

        best = current.copy()
        best_score = current_score

        # Auto-scaling
        temperature = (
            self.initial_temperature
            if self.initial_temperature is not None
            else self._estimate_initial_temperature(problem)
        )
        cooling_rate = (
            self.cooling_rate
            if self.cooling_rate is not None
            else self._estimate_cooling_rate(temperature)
        )

        print(f"SA init temp: {temperature:.2f}, cooling rate: {cooling_rate:.6f}")

        for _ in range(self.iterations):
            candidate = problem.neighbor(current)
            candidate_score = problem.evaluate(candidate)
            delta = candidate_score - current_score

            if delta < 0:
                current = candidate
                current_score = candidate_score
                accepted_better += 1
            else:
                probability = math.exp(-delta / temperature)
                if random.random() < probability:
                    current = candidate
                    current_score = candidate_score
                    accepted_worse += 1

            if current_score < best_score:
                best = current.copy()
                best_score = current_score

            temperature *= cooling_rate
            if temperature < 1e-8:
                break

            history.append(best_score)

        print(f"Better accepted: {accepted_better}")
        print(f"Worse accepted:  {accepted_worse}")
        return best, best_score, history