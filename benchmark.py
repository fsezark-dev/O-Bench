import statistics
import time

def benchmark(optimizer, problem, trials=30):
    scores = []
    histories = []
    runtimes = []

    for _ in range(trials):
        start = time.perf_counter()
        _, score, history = optimizer.solve(problem)
        end = time.perf_counter()

        scores.append(score)
        histories.append(history)
        runtimes.append(end - start)

    return {
        "best": min(scores),
        "worst": max(scores),
        "mean": statistics.mean(scores),
        "std": statistics.stdev(scores),
        "scores": scores,
        "histories": histories,
        "runtime": sum(runtimes) / len(runtimes),
    }