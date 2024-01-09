from itertools import product

import altair as alt
import pandas as pd


class Result:
    """
    Class for storing and plotting simulation results.

    Arguments:
    ----------
    data : dataframe (required)
        Dataframe with simulation results.
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def get_data(self):
        """Return dataframe with simulation results."""
        return self.data

    def _single_plot(
        self,
        data,
        x="sample_size",
        y="power",
        title=None,
        color="evaluator",
        hline_pos="0.8",
    ):
        """Print a power graph.

        Parameters
        ----------
        data : dataframe (required)
            name of dataframe
        x : string (optional)
            name of x coordinate (sample size), default is 'sample_size'
        y : string (optional)
            name of y coordinate (power), default is 'power'
        color : string (optional)
            name of variable for color encoding, default is 'test'
        hline_pos : str of float (optional)
            position of horizontal line to indicate target power level, default is '0.8'

        Returns
        -------
        Altair plot: A plot showing level of power for each sample size for each evaluator.
        """
        dots = (
            alt.Chart(data)
            .mark_point()
            .encode(
                x=alt.X(x, axis=alt.Axis(title="Sample size")),
                y=alt.Y(y, axis=alt.Axis(title="Power")),
                color=alt.Color(color, legend=alt.Legend(title="Evaluator")),
            )
        )
        loess = dots.transform_loess(x, y, groupby=[color]).mark_line()
        hline = (
            alt.Chart(self.data)
            .mark_rule(color="red")
            .encode(
                y=alt.Y("a:Q", axis=alt.Axis(title="")),
            )
            .transform_calculate(a=hline_pos)
        )
        plot = dots + loess + hline
        if title:
            plot = plot.properties(title=title)
        return plot

    def plot(self):
        mdes_values = self.data["mdes"].unique()
        metric_names = self.data["metric"].unique()
        tasks = product(metric_names, mdes_values)
        plots = []
        for metric, mdes in tasks:
            mask = (self.data["metric"] == metric) & (self.data["mdes"] == mdes)
            data = self.data[mask]
            plot = self._single_plot(
                data,
                title=f"{metric}, MDES = {mdes:.0%}",
            )
            plots.append(plot)
        return alt.vconcat(*plots)
