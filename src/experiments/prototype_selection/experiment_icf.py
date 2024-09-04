from src.utils.result import log_result
from src.utils.data_preprocessing import load_data
from src.utils.evaluation_metrics import compare_prototype_selection

from src.algorithms.prototype_selection.drop3 import DROP3
from src.algorithms.prototype_selection.icf import ICF

DATASET_NAME = "wine"

# Get file name
from src.utils.path import ProjectPath

FILE_NAME = ProjectPath(__file__).get_safe_filename()

# Load dataset
X, y = load_data(DATASET_NAME)

# Define the algorithms
algorithms = {
    "DROP3": {"algorithm": DROP3().fit_transform},
    "ICF": {"algorithm": ICF().fit_transform},
}

k, n_folds = 1, 10

result = compare_prototype_selection(X, y, algorithms, k, n_folds)

result = {
    "Dataset": DATASET_NAME,
    "k": k,
    "n_folds": n_folds,
    "results": result,
}

log_result(result, FILE_NAME)
