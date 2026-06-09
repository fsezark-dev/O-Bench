def average_history(histories):
    iterations = len(histories[0])

    avg = []

    for i in range(iterations):
        avg.append(
            sum(history[i] for history in histories)/ len(histories)
        )

    return avg
