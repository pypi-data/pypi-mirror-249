import scipy
import typing
from glidergun.core import Grid, _batch, _focal


class StatsResult(typing.NamedTuple):
    statistic: Grid
    pvalue: Grid


def focal_chisquare(buffer: int, circle: bool, grid: Grid, **kwargs) -> StatsResult:
    def f(grids):
        return _focal(
            lambda a: scipy.stats.chisquare(a, axis=2, **kwargs),
            buffer,
            circle,
            *grids,
        )

    return StatsResult(*_batch(f, buffer, grid))


def focal_f_oneway(buffer: int, circle: bool, *grids: Grid, **kwargs) -> StatsResult:
    def f(grids):
        return _focal(
            lambda a: scipy.stats.f_oneway(*a, axis=2, **kwargs),
            buffer,
            circle,
            *grids,
        )

    return StatsResult(*_batch(f, buffer, *grids))


def focal_ttest_ind(
    buffer: int, circle: bool, grid1: Grid, grid2: Grid, **kwargs
) -> StatsResult:
    def f(grids):
        return _focal(
            lambda a: scipy.stats.ttest_ind(*a, axis=2, **kwargs),
            buffer,
            circle,
            *grids,
        )

    return StatsResult(*_batch(f, buffer, grid1, grid2))
