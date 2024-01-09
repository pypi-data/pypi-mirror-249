import pandas as pd

from cumulative.transforms.transform import Transform


class Select(Transform):
    def transform_row(self, row, src, func=lambda x: x):

        s = pd.Series(row[f"{src}.y"], index=row[f"{src}.x"])
        s = func(s)

        return pd.Series({"x": s.index.values, "y": s.values})
