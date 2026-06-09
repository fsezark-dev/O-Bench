from collections import deque

class TabuSearch:

    def __init__(
        self,
        iterations=1000,
        tabu_size=20
    ):
        self.iterations = iterations
        self.tabu_size = tabu_size

    def solve(self, problem):

        history = []

        current = problem.random_solution()
        current_score = problem.evaluate(current)

        best = current.copy()
        best_score = current_score

        tabu_list = deque(maxlen=self.tabu_size)

        for _ in range(self.iterations):

            best_candidate = None
            best_candidate_score = float("inf")

            for _ in range(50):  # neighborhood size

                candidate = problem.neighbor(current)

                candidate_key = tuple(candidate)

                if candidate_key in tabu_list:
                    continue

                score = problem.evaluate(candidate)

                if score < best_candidate_score:
                    best_candidate = candidate
                    best_candidate_score = score

            if best_candidate is None:
                break

            current = best_candidate
            current_score = best_candidate_score

            tabu_list.append(tuple(current))

            if current_score < best_score:
                best = current.copy()
                best_score = current_score

            history.append(best_score)

        return best, best_score, history