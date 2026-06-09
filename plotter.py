from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


class ConvergencePlotter:
    def __init__(self, output_dir="results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_convergence_plot(self, curves, filename="convergence", ylabel="Best Distance", title="Average Convergence (30 Runs)"):
        plt.figure(figsize=(10, 6))

        for label, curve in curves.items():
            plt.plot(curve, label=label)

        plt.xlabel("Iteration")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid(True)

        plt.savefig(
            self.output_dir / f"{filename}.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.close()


    def save_convergence_csv(self, curves, filename="convergence"):
        csv_path = self.output_dir / f"{filename}.csv"
        max_len = max(len(curve) for curve in curves.values())

        data = {
            "Iteration": range(max_len)
        }

        for label, curve in curves.items():
            data[label] = curve

        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)