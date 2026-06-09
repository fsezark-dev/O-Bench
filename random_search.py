class RandomSearch:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def solve(self, problem):
        history=[]
        best_solution = None
        best_score = float('inf')
        for _ in range(self.iterations):
            solution = problem.random_solution()
            score = problem.evaluate(solution)

            if score < best_score:
                best_solution = solution.copy()
                best_score = score
            history.append(best_score)
        return best_solution, best_score, history