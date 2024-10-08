import numpy as np
from sklearn.metrics import pairwise_distances
from src.algorithms.prototype_selection.base import BaseAlgorithm
from src.algorithms.prototype_selection.enn import ENN


class ICF(BaseAlgorithm):
    """
    Iterative case filtering (ICF)
    """

    def __init__(self, n_neighbors: int = 3, metric="euclidean"):
        super().__init__()
        self.metric = metric
        self.n_neighbors = n_neighbors
        self.mask: np.ndarray = None
        self.distance_nearest_enemy: np.ndarray = None
        self.pairwise_distance: np.ndarray = None

    def _set_distance_nearest_enemy(self):
        """
        Set the minimum distance to the nearest enemy for each instance.
        """

        self.distance_nearest_enemy = np.full(self.X_.shape[0], np.inf)

        for idx in range(self.X_.shape[0]):
            for idx2 in range(self.X_.shape[0]):
                if (
                    self.y_[idx] != self.y_[idx2]
                    and self.pairwise_distance[idx, idx2]
                    < self.distance_nearest_enemy[idx]
                ):
                    self.distance_nearest_enemy[idx] = self.pairwise_distance[idx, idx2]

    def _adaptable(self, idx: int, idx2: int) -> bool:
        """
        Check if an instance is adaptable to another instance.

        Parameters:
        idx (int): Index of the first instance.
        idx2 (int): Index of the second instance.

        Returns:
        bool: True if the instance is adaptable, False otherwise.
        """
        # TODO: Check if nearest enemy if for idx or idx2
        return self.pairwise_distance[idx, idx2] < self.distance_nearest_enemy[idx2]

    def _get_coverage(self, idx: int) -> int:
        """
        Get the number of instances covered by a given instance.

        Parameters:
        idx (int): Index of the instance.

        Returns:
        int: Number of instances covered.
        """
        len_coverage = 0

        for idx2 in range(self.X_.shape[0]):
            if idx2 != idx and self.mask[idx2]:
                if self._adaptable(idx, idx2):
                    len_coverage += 1

        return len_coverage

    def _get_reachable(self, idx: int) -> int:
        """
        Get the number of reachable instances for a given instance.

        Parameters:
        idx (int): Index of the instance.

        Returns:
        int: Number of reachable instances.
        """
        len_reachable = 0

        for idx2 in range(self.X_.shape[0]):
            if idx2 != idx and self.mask[idx2]:
                if self._adaptable(idx2, idx):
                    len_reachable += 1

        return len_reachable

    def _fit(self) -> np.ndarray:
        """
        Select instances from the training data.

        Returns:
        np.ndarray: Indices of the selected instances.
        """
        S = ENN(self.n_neighbors).fit(self.X, self.y).sample_indices_

        progress = True

        while progress:
            self.X_ = self.X[S]
            self.y_ = self.y[S]

            self.pairwise_distance = pairwise_distances(self.X_, metric=self.metric)

            self._set_distance_nearest_enemy()

            self.mask = np.ones(len(self.X_), dtype=bool)

            reachable, coverage = np.zeros(len(self.X_)), np.zeros(len(self.X_))
            for idx in range(self.X_.shape[0]):
                if self.mask[idx]:
                    coverage[idx] = self._get_coverage(idx)
                    reachable[idx] = self._get_reachable(idx)

            progress = False

            for idx in range(self.X_.shape[0]):
                if self.mask[idx] and reachable[idx] > coverage[idx]:
                    self.mask[idx] = False
                    progress = True

            S = S[self.mask]

        return S
