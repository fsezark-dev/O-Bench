class HillClimbing:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def solve(self, problem):
        history = []
        current = problem.random_solution()
        current_score = problem.evaluate(current)

        best = current.copy()
        best_score = current_score

        for _ in range(self.iterations):

            candidate = problem.neighbor(current)
            candidate_score = problem.evaluate(candidate)

            if candidate_score < current_score:
                current = candidate
                current_score = candidate_score

                if current_score < best_score:
                    best = current.copy()
                    best_score = current_score
            history.append(best_score)
        return best, best_score, history