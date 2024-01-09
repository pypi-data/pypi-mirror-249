def no_missing_values(df, metrics):
    """Ensure there are no missing values in metric columns.

    Rationale:
    - Presence of missing values dilute power because effective
      sample size is going to be smaller than reported one.
    - In datasets with many missing values, which are common in
      practice, this can lead to situations where reported power
      is zero, because all randomly sampled units at each sample
      size had missing data.
    """
    print(len(df.dropna(subset=metrics)), len(df))
    if len(df.dropna(subset=metrics)) != len(df):
        raise ValueError(
            "Metric values cannot be missing as this would impact simulation results."
        )


def sample_min_max_specified(sample_min, sample_max):
    if (sample_max is None) ^ (sample_min is None):
        raise ValueError(
            "Both or neither of sample_max and sample_min must be specified."
        )


def sample_min_max_valid(sample_min, sample_max):
    if (sample_min and sample_max) and (sample_min > sample_max):
        raise ValueError("Min sample size cannot be larger than max sample size.")


def sample_min_max_size(
    df, time_col, id_col, sample_timestamps, sample_min, sample_max
):
    if (sample_timestamps and sample_max) and (df[time_col].nunique() < sample_max):
        raise ValueError(
            "Max sample size cannot be larger than number of time periods in the data."
        )

    if (not sample_timestamps and sample_max) and (df[id_col].nunique() < sample_max):
        raise ValueError(
            "Max sample size cannot be larger than number of units in the data."
        )


def evaluator_supplied(evaluators):
    if not evaluators:
        raise ValueError("At least one evaluator must be specified.")


def evaluator_names_unique(evaluators):
    if len(evaluators) != len(set(evaluators)):
        raise ValueError("Evaluator names must be unique.")


def preprocessor_names_unique(preprocessors):
    if len(preprocessors) != len(set(preprocessors)):
        raise ValueError("Preprocessor names must be unique.")
