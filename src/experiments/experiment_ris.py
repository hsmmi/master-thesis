import random
from src.utils.evaluation_metrics import compare_prototype_selection
from src.algorithms.ris import RIS as RIS
from src.algorithms.drop3 import DROP3 as DROP3

import tabulate
from sklearn.datasets import load_wine

# set random seed to 42
random.seed(42)

# Load wine dataset
data = load_wine()
X, y = data.data, data.target

# Scale the data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Define the algorithms
algorithms = {
    "DROP3": {"algorithm": DROP3(3).fit_transform},
    "RIS1": {"algorithm": RIS("RIS1", 0.1).fit_transform},
    "RIS2": {"algorithm": RIS("RIS2", 0.1).fit_transform},
    "RIS3": {"algorithm": RIS("RIS3", 0.1).fit_transform},
}

result = compare_prototype_selection(X, y, algorithms, 3, 10)

# Log the results
log_path = "results/logs/experiment_ris.log"

formatted_result = {
    key: {
        "Accuracy": result[key][0],
        "Size": result[key][1],
        "Reduction": result[key][2],
        "Time": result[key][3],
    }
    for key in result
}

with open(log_path, "a") as f:
    f.write(str(formatted_result) + "\n")

# Print in tabulated format
table = []
for key in result:
    table.append(
        [
            key,
            f"{result[key][0]*100:.2f}%",
            result[key][1],
            f"{result[key][2]*100:.2f}%",
            f"{result[key][3]:.2f}s",
        ]
    )

headers = [
    "Algorithm",
    "Accuracy",
    "Size",
    "Reduction",
    "Time",
]

# Add padding to the headers :^10
headers = [f"{header:^10}" for header in headers]

print(
    tabulate.tabulate(
        table,
        headers,
        tablefmt="fancy_grid",
        colalign=["center"] * 5,
    )
)
