import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import Tuple
from glidergun.core import Grid, _standardize, con


def scale(grid: Grid, **fit_params) -> Grid:
    return grid.local(lambda a: StandardScaler().fit_transform(a, **fit_params))


def pca(n_components: int = 1, *grids: Grid) -> Tuple[Grid, ...]:
    grids_adjusted = [con(g.is_nan(), g.mean, g) for g in _standardize(True, *grids)]
    arrays = (
        PCA(n_components=n_components)
        .fit_transform(
            np.array([scale(g).data.ravel() for g in grids_adjusted]).transpose((1, 0))
        )
        .transpose((1, 0))
    )
    grid = grids_adjusted[0]
    return tuple(grid._create(a.reshape((grid.height, grid.width))) for a in arrays)
