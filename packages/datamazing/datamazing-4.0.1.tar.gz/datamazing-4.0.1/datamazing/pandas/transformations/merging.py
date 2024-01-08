from functools import reduce

import pandas as pd

from datamazing.pandas.transformations import basic


def merge_many(
    dfs: list[pd.DataFrame],
    on: list[str],
    how: str = "inner",
) -> pd.DataFrame:
    return reduce(lambda df1, df2: df1.merge(df2, on=on, how=how), dfs)


def merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_on: list[str] | None = None,
    right_on: list[str] | None = None,
    on: list[str] | None = None,
    left_time: str | None = None,
    right_period: tuple[str, str] | None = None,
    how: str = "inner",
):
    if bool(left_time) != bool(right_period):
        raise ValueError(
            "Both `left_time` and `right_period` must be set when time-merging"
        )

    if left_time and right_period:
        if how != "inner":
            raise ValueError('Only `how="inner"` is supported when time-merging')

        # sort values in order to use `pd.merge_asof`
        left = left.sort_values(by=left_time)

        right = basic.fill_empty_periods(df=right, period=right_period)
        right = right.sort_values(by=right_period[0])

        # make left-join, matching the latest right-start-time
        # which is below the left-time
        df = pd.merge_asof(
            left,
            right,
            left_on=left_time,
            right_on=right_period[0],
            left_by=left_on,
            right_by=right_on,
            by=on,
        )

        # remove matches, where the right-end-time is also below the left-time.
        df = df[df[left_time] < df[right_period[1]]]

        # remove records with no matches (this is necessary, since
        # `pd.merge_asof` always does a left-join, but we want an inner-join)

    else:
        df = pd.merge(left, right, left_on=left_on, right_on=right_on, on=on, how=how)

    return df
