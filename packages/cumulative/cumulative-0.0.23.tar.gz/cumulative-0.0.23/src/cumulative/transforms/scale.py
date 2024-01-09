import logging

import pandas as pd

from cumulative.transforms.transform import Transform

log = logging.getLogger(__name__)


class ExceptionScaler(Exception):
    pass


class Scale(Transform):
    """
    MinMax normalizer on x,y axes to the unit interval [0,1].
    If the sequence contains less than two distinct values, all values are set to 1.
    """

    def transform_row(self, row, src):

        s = pd.Series(row[f"{src}.y"], index=row[f"{src}.x"])

        if len(s) == 0:
            raise ExceptionScaler(f"idx={row['idx']}: series length is zero")

        attrs = {
            "x_min": s.index.min(),
            "x_max": s.index.max(),
            "y_min": s.min(),
            "y_max": s.max(),
        }

        if len(s) == 1:
            log.warning(f"idx={row['idx']}: series length is below 2 (normalized to unit)")
            # Using 1 as default normalised value, to have integrals summing up to 1.
            s[:] = 1
        elif s.nunique() < 2:
            log.warning(f"idx={row['idx']}: series contains less than 2 distinct values (normalized to unit)")
            # Using 1 as default normalised value, to have integrals summing up to 1.
            s[:] = 1
        else:
            s = s - s.min()
            s = s / s.max()

        s.index -= s.index.min()
        s.index /= s.index.max()

        attrs = {
            **attrs,
            **{
                "x": s.index.values,
                "y": s.values,
            },
        }

        return pd.Series(attrs)
