import matplotlib
import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt

from cumulative.options import options


class Figure:
    def __init__(self, x_label="X", y_label="Y", ioff=False):
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.rcParams["font.family"] = "monospace"
        cmap = matplotlib.colormaps["cool"]

        if ioff:
            plt.ioff()
        else:
            plt.ion()

        fig, ax = plt.subplots(figsize=(5, 5))

        ax.clear()
        ax.set_facecolor("black")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        lim_pad = 0.05
        ax.set_xlim(0 - lim_pad, 1 + lim_pad)
        ax.set_ylim(0 - lim_pad, 1 + lim_pad)

        self.fig = fig
        self.ax = ax
        self.cmap = cmap


class Plot:
    def __init__(self, c):
        self.c = c

    def xrays(self, src=None, alpha=1, ms=1, lw=1, k=60, style=".", show=True):
        src = options.default_if_null(src, "transforms.source")
        tmp = options.get("transforms.tmp")
        with options.option_context({"transforms": {"source": tmp, "destination": tmp}}):
            self.c.fit(src=src, method="pchip3", k=k, n_samples=k)
            self.c.plot.scatter(alpha=alpha, ms=ms, lw=lw, style=style)
            self.c.drop()

    def heatmap(self, src=None, ms=4, k=60, score="idx", style=".", show=True):
        src = options.default_if_null(src, "transforms.source")
        tmp = options.get("transforms.tmp")
        tmp_score = f"{tmp}.score"
        with options.option_context({"transforms": {"source": tmp, "destination": tmp}}):
            self.c.fit(src=src, method="pchip3", k=k, n_samples=k)
            self.c.score(src=score, dst=tmp_score).sort(by=tmp_score)
            self.c.plot.scatter(ms=ms, alpha=tmp_score, score=tmp_score, style=style)
            self.c.drop()

    def highways(self, src=None, ms=4, k=60, score="idx", style=".", show=True):
        src = options.default_if_null(src, "transforms.source")
        tmp = options.get("transforms.tmp")
        tmp_score = f"{tmp}.score"
        with options.option_context({"transforms": {"source": tmp, "destination": tmp}}):
            # TODO: move sort to internals of scatter(), without sorting c.df
            self.c.score(src=score, dst=tmp_score).sort(by=tmp_score)
            self.c.plot.scatter(src=src, alpha=1, score=tmp_score, lw=1, style="-")
            self.c.drop()

    def pixelate(self, src=None, k=30, alpha=0.05, ms=5, style="s", show=True):
        src = options.default_if_null(src, "transforms.source")
        tmp = options.get("transforms.tmp")
        with options.option_context({"transforms": {"source": tmp, "destination": tmp}}):
            self.c.interp(n_samples=k, src=src)
            self.c.bin(n_bins=k)
            self.c.fit(method="pchip3", k=k, n_samples=k)
            self.c.plot.scatter(alpha=alpha, ms=ms, style=style)
            self.c.drop()

    def scatter(
        self, src=None, style=".", ms=2, lw=1, score=None, alpha=0.5, figure=None, x_label="x", y_label="y", show=True
    ):

        src = options.default_if_null(src, "transforms.source")

        if figure is None:
            figure = Figure(x_label=x_label, y_label=y_label)

        for _, row in self.c.df.iterrows():
            row_color = figure.cmap(row[score]) if isinstance(score, str) else "white"
            row_alpha = row[alpha] if isinstance(alpha, str) else alpha
            pd.Series(row[f"{src}.y"], index=row[f"{src}.x"]).plot(
                style=style,
                lw=lw,
                ms=ms,
                color=row_color,
                alpha=row_alpha,
                ax=figure.ax,
            )

        if show and plt.isinteractive():
            plt.show()
