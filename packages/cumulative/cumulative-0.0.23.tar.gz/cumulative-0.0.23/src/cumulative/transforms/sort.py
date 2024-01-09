from cumulative.transforms.transform import Transform


class Sort(Transform):
    def apply(self, by, ascending=True):
        self.c.df = self.c.df.sort_values(by=by, ascending=ascending)
