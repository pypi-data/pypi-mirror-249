import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform


class Integrate(Transform):
    def transform_row(self, row, src, normalize=True):

        s = pd.Series(np.cumsum(row[f"{src}.y"]), index=row[f"{src}.x"])

        attrs = {}

        if normalize:
            s -= s.min()
            s /= s.max()

        attrs["x"] = row[f"{src}.x"]
        attrs["y"] = s.values

        return pd.Series(attrs)
