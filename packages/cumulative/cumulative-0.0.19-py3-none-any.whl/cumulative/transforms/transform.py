import logging

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from cumulative.options import options

log = logging.getLogger(__name__)


def process_row(func, row, **kwargs):
    return func(row, **kwargs)


class Transform:
    def __init__(self, c, name=None):
        self.c = c
        self.name = self.__class__.__name__.lower() if not name else name

    def transform_row(self, row):
        return pd.Series()

    def __call__(self, **kwargs):
        tqdm_params = options.get("tqdm.params")
        tqdm_params["desc"] = self.name
        tqdm.pandas(**tqdm_params)
        # The destination prefix is not required/expected by row transforms,
        # let's drop it if present.

        dst = options.default_if_null(kwargs.pop("dst", None), "transforms.destination")

        kwargs["src"] = options.default_if_null(kwargs.pop("src", None), "transforms.source")

        df = self.apply(**kwargs)

        self.c.track(self.name, dst, kwargs)

        if df is None:
            # Sort
            return self.c

        if isinstance(df, pd.DataFrame):
            df.columns = [f"{dst}.{col}" if col != "idx" else col for col in df.columns]
        elif isinstance(df, pd.Series):
            df = df.rename(dst).to_frame()
        else:
            raise Exception("Invalid argument type")

        self.validate(df)

        drop_cols = self.c.columns_with_prefix(dst, errors="ignore")
        self.c.df = self.c.df.drop(columns=drop_cols, errors="ignore")
        self.c.df = pd.concat(
            [self.c.df, df],
            axis=1,
        )
        return self.c

    def apply(self, **kwargs):
        return self.c.df.progress_apply(lambda row: self.transform_row(row, **kwargs), axis=1)

    def validate(self, df):
        # Check for invalid values (nans, infs)
        count_rows = len(df)
        count_invalid_rows = df.isin([np.inf, -np.inf, np.nan]).any(axis=1).sum()
        if count_invalid_rows > 0:
            log.warning(
                f"{self.name} produced {count_invalid_rows} ({count_invalid_rows / count_rows * 100:.0f}%)"
                " invalid rows (nans or infs)"
            )

        if len(set(df.columns)) != len(df.columns):
            log.warning(f"{self.name} produced duplicate column names")

        if len(df.columns) == 0:
            log.warning(f"{self.name} produced no columns")

        if len(df) == 0:
            log.warning(f"{self.name} produced no rows")
