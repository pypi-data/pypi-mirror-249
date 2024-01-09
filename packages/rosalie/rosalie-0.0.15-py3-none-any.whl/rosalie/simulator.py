"""
Simulator class.
"""

from collections import namedtuple
from copy import copy
from typing import (
    Callable,
    List,
    Optional,
)

import numpy as np
import pandas as pd
from tqdm import tqdm

from .utils.input_checks import (
    evaluator_names_unique,
    evaluator_supplied,
    no_missing_values,
    preprocessor_names_unique,
    sample_min_max_size,
    sample_min_max_specified,
    sample_min_max_valid,
)
from .utils.logger import module_logger
from .utils.result import Result

logger = module_logger(__name__)


ExperimentResult = namedtuple(
    "ExperimentResult",
    ["metric", "preprocessor", "evaluator", "sample_size", "mdes", "power"],
)


class Simulator:
    """
    Class to simulate experiments.

    Arguments:
    ----------
    df : dataframe (required)
        Dataframe with simulation results.
    evaluators : list of callables (optional)
        List of evaluators to use, default is None. If no evaluators are
        specified, then a baseline evaluator must be specified.
    preprocessors : list of callables (optional)
        List of preprocessors to use, default is None, in which case passed
        data is not processed before being passed to evaluators.
    id_col : string (optional)
        Name of column with unit IDs, default is 'id'.
    time_col : string (optional)
        Name of column with time periods, default is 'timeframe'.
    metrics : list of strings (optional)
        Names of metrics to evaluate, default is ['y'].
    sample_min : int (optional)
        Minimum sample size to simulate, default is None.
    sample_max : int (optional)
        Maximum sample size to simulate, default is None.
    num_steps : int (optional)
        Number of sample sizes to simulate, default is 10.
    sample_timestamps : bool (optional)
        Whether to sample timestamps instead of units, default is False.
    num_runs : int (optional)
        Number of runs to simulate for each sample size, default is 20.
    random_seed : int (optional)
        Random seed to use, default is 2312.
    mdes : list of floats (optional)
        List of minimum detectable effects to simulate, default is [0.02].
    alpha : float (optional)
        Significance level to use, default is 0.05.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        evaluators: Optional[List[Callable]] = None,
        preprocessors: Optional[List[Callable]] = None,
        id_col: Optional[str] = "id",
        time_col: Optional[str] = "timeframe",
        metrics: Optional[List[str]] = ["y"],
        sample_min: Optional[int] = None,
        sample_max: Optional[int] = None,
        num_steps: Optional[int] = 20,
        sample_timestamps: Optional[bool] = False,
        num_runs: Optional[int] = 50,
        random_seed: Optional[int] = 2312,
        mdes: Optional[List[float]] = [0.01],
        alpha: Optional[float] = 0.05,
        verbose: Optional[bool] = True,
    ):
        self.df = df
        self.evaluators = evaluators or []
        self.preprocessors = preprocessors or []
        self.id_col = id_col
        self.time_col = time_col
        self.metrics = metrics
        self.sample_min = sample_min
        self.sample_max = sample_max
        self.num_steps = num_steps
        self.sample_timestamps = sample_timestamps
        self.num_runs = num_runs
        self.random_seed = random_seed
        self.mdes = mdes
        self.alpha = alpha

        self.has_preprocessors = len(self.preprocessors) > 0
        self.rng = np.random.default_rng(self.random_seed)

        self._check_input()
        self._set_defaults()
        if verbose:
            self._print_user_info()

    def run(self):
        """Run simulation."""
        results = []
        for preprocessor in self.preprocessors:
            df_preproc = preprocessor(self.df)
            for sample_size in tqdm(self._calc_sample_sizes()):
                sample_func = self._get_sample_func()
                df_sample = sample_func(df_preproc, sample_size)
                for _ in range(self.num_runs):
                    df_assigned = self._create_treatment_assignments(df_sample)
                    for mdes in self.mdes:
                        df_effect = self._add_treatment_effect(
                            df_assigned, self.metrics, mdes
                        )
                        for metric in self.metrics:
                            for evaluator in self.evaluators:
                                p = evaluator(df_effect, metric)
                                is_statsig = p <= self.alpha
                                result = ExperimentResult(
                                    metric=metric,
                                    preprocessor=preprocessor.__name__,
                                    evaluator=evaluator.__name__,
                                    sample_size=sample_size,
                                    mdes=mdes,
                                    power=is_statsig,
                                )
                                results.append(result)

        result_cols = self._get_result_cols()
        result = Result(
            pd.DataFrame(results)
            .loc[:, result_cols]
            .groupby(result_cols[:-1])
            .mean()
            .reset_index()
            .sort_values(result_cols)
        )
        return result

    def _create_treatment_assignments(self, df):
        """Add columns with treatment assignments to dataframe."""
        unique_ids = df[self.id_col].unique()
        assignments = self.rng.choice([True, False], size=len(unique_ids))
        labels = {True: "treatment", False: "control"}
        id_to_assignment = dict(zip(unique_ids, assignments))

        df["is_treated"] = df[self.id_col].map(id_to_assignment)
        df["assignments"] = df["is_treated"].map(labels)
        df["assignments_freq"] = 1

        return df

    def _add_treatment_effect(self, df, metrics, mdes):
        """Add column with artificial treatment effect to dataframe."""
        df = df.copy()
        effect_map = {"control": 1.0, "treatment": (1 + mdes)}
        multiplier = df["assignments"].map(effect_map)
        df[metrics] = df[metrics].mul(multiplier, axis=0)
        return df

    def _sample_timestamps(self, df, sample_size):
        """Sample timestamps from dataframe."""
        unique_timestamps = sorted(df[self.time_col].unique())
        sample_timestamps = unique_timestamps[:sample_size]
        return df[df[self.time_col].isin(sample_timestamps)].copy()

    def _sample_users(self, df, sample_size):
        """Sample users from dataframe."""
        unique_ids = df[self.id_col].unique()
        sample_ids = self.rng.choice(unique_ids, sample_size, replace=False)
        return df[df[self.id_col].isin(sample_ids)].copy()

    def _calc_sample_sizes(self):
        """Calculate sample sizes to simulate."""
        return (
            np.linspace(self.sample_min, self.sample_max, self.num_steps)
            .round()
            .astype(int)
        )

    def _get_sample_func(self):
        return self._sample_timestamps if self.sample_timestamps else self._sample_users

    def _evaluator_names(self):
        """Return names of evaluators."""
        return [func.__name__ for func in self.evaluators]

    def _preprocessor_names(self):
        """Return names of preprocessors."""
        return [func.__name__ for func in self.preprocessors]

    def _dummy_preprocessor(self, df):
        """Return unprocessed data."""
        return df

    def _get_result_cols(self):
        """Return names of columns in result dataframe."""
        cols = list(ExperimentResult._fields)
        if not self.has_preprocessors:
            cols.remove("preprocessor")
        return cols

    def _check_input(self):
        """Check input."""
        no_missing_values(self.df, self.metrics)
        sample_min_max_specified(self.sample_min, self.sample_max)
        sample_min_max_valid(self.sample_min, self.sample_max)
        sample_min_max_size(
            self.df,
            self.time_col,
            self.id_col,
            self.sample_timestamps,
            self.sample_min,
            self.sample_max,
        )
        evaluator_supplied(self.evaluators)
        evaluator_names_unique(self.evaluators)
        preprocessor_names_unique(self.preprocessors)

    def _set_defaults(self):
        """Set default values."""
        if not self.sample_max and not self.sample_min:
            self._set_sample_sizes()

        if not self.has_preprocessors:
            self._add_dummy_preprocessor()

    def _set_sample_sizes(self):
        if self.sample_timestamps:
            self.sample_max = self.df[self.time_col].nunique()
            self.sample_min = 1
        else:
            self.sample_max = self.df[self.id_col].nunique()
            self.sample_min = min(100, self.sample_max)

    def _add_dummy_preprocessor(self):
        """Add dummy preprocessor if none specified."""
        self.preprocessors = copy(self.preprocessors)
        self.preprocessors = [self._dummy_preprocessor]

    def _print_user_info(self):
        """Print user info."""

        logger.info(
            f"Initializing Simulator with specified evaluators: {self._evaluator_names()}"
        )
        if self.has_preprocessors:
            logger.debug(
                f"Specified preprocessors for Simulator: {self._preprocessor_names()}"
            )
