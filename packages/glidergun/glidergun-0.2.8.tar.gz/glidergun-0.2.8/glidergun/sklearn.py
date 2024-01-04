import numpy as np
import sklearn.decomposition
import sklearn.ensemble
import sklearn.linear_model
import sklearn.pipeline
import sklearn.preprocessing
import sklearn.svm
import sklearn.tree
import typing
from glidergun.core import Grid, _standardize, con


def scale(grid: Grid, **fit_params) -> Grid:
    return grid.local(
        lambda a: sklearn.preprocessing.StandardScaler().fit_transform(a, **fit_params)
    )


def pca(n_components: int = 1, *grids: Grid) -> typing.Tuple[Grid, ...]:
    grids_adjusted = [con(g.is_nan(), g.mean, g) for g in _standardize(True, *grids)]
    arrays = (
        sklearn.decomposition.PCA(n_components=n_components)
        .fit_transform(
            np.array([scale(g).data.ravel() for g in grids_adjusted]).transpose((1, 0))
        )
        .transpose((1, 0))
    )
    grid = grids_adjusted[0]
    return tuple(grid._create(a.reshape((grid.height, grid.width))) for a in arrays)


class Regressor(typing.Protocol):
    fit: typing.Callable
    score: typing.Callable
    predict: typing.Callable


T = typing.TypeVar("T", bound=Regressor)


class RegressionProvider(typing.Generic[T]):
    def __init__(
        self, model: T, dependent_grid: Grid, *explanatory_grids: Grid
    ) -> None:
        head, *tail = self._flatten(dependent_grid, *explanatory_grids)
        self._model = model.fit(
            np.array([g.data.ravel() for g in tail]).transpose(1, 0), head.data.ravel()
        )

    def _flatten(self, *grids: Grid):
        return [con(g.is_nan(), g.mean, g) for g in _standardize(True, *grids)]

    def score(self, dependent_grid: Grid, *explanatory_grids: Grid) -> float:
        head, *tail = self._flatten(dependent_grid, *explanatory_grids)
        return self._model.score(
            np.array([g.data.ravel() for g in tail]).transpose(1, 0), head.data.ravel()
        )

    def predict(self, *explanatory_grids: Grid) -> Grid:
        grids = self._flatten(*explanatory_grids)
        array = self._model.predict(
            np.array([g.data.ravel() for g in grids]).transpose(1, 0)
        )
        grid = grids[0]
        return grid._create(array.reshape((grid.height, grid.width)))


def decision_tree(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.tree.DecisionTreeRegressor(**kwargs), dependent_grid, *explanatory_grids
    )


def lasso(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.linear_model.Lasso(**kwargs), dependent_grid, *explanatory_grids
    )


def linear(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.linear_model.LinearRegression(**kwargs),
        dependent_grid,
        *explanatory_grids
    )


def polynomial(dependent_grid: Grid, *explanatory_grids: Grid):
    return RegressionProvider(
        sklearn.pipeline.Pipeline(
            [
                ("polynomial", sklearn.preprocessing.PolynomialFeatures(degree=2)),
                ("linear", sklearn.linear_model.LinearRegression()),
            ]
        ),
        dependent_grid,
        *explanatory_grids
    )


def random_forest(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.ensemble.RandomForestRegressor(**kwargs),
        dependent_grid,
        *explanatory_grids
    )


def ridge(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.linear_model.Ridge(**kwargs), dependent_grid, *explanatory_grids
    )


def svr(dependent_grid: Grid, *explanatory_grids: Grid, **kwargs):
    return RegressionProvider(
        sklearn.svm.SVR(**kwargs), dependent_grid, *explanatory_grids
    )
