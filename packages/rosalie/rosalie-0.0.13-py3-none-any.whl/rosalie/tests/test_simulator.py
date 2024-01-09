import pandas as pd
import pytest

from rosalie import Simulator

# Fixtures


@pytest.fixture
def df_sample():
    data = {
        "id": list(range(1, 101)),
        "y": list(range(100)),
        "timeframe": ["2021-01-01", "2021-01-02"] * 50,
    }
    return pd.DataFrame(data)


@pytest.fixture
def evaluator_instance(df_sample):
    return Simulator(df_sample, baseline_evaluator="wls")


# Unit Tests


def test_evaluator_names(evaluator_instance):
    assert set(evaluator_instance._evaluator_names()) == {"wls"}


def test_preprocessor_names(evaluator_instance):
    assert set(evaluator_instance._preprocessor_names()) == {"_dummy_preprocessor"}


def test_dummy_preprocessor(evaluator_instance, df_sample):
    assert evaluator_instance._dummy_preprocessor(df_sample).equals(df_sample)


def test_create_treatment_assignments(evaluator_instance, df_sample):
    df_assigned = evaluator_instance._create_treatment_assignments(df_sample)
    assert "is_treated" in df_assigned.columns
    assert "assignments" in df_assigned.columns
    assert "assignments_freq" in df_assigned.columns
    assert set(df_assigned["is_treated"].unique()) == {True, False}
    assert set(df_assigned["assignments"].unique()) == {"treatment", "control"}


def test_add_treatment_effect(evaluator_instance, df_sample):
    df_assigned = evaluator_instance._create_treatment_assignments(df_sample)
    treat_pre_effect = df_assigned.query("is_treated == True")
    control_pre_effect = df_assigned.query("is_treated == False")
    df_effect = evaluator_instance._add_treatment_effect(df_assigned, "y", 0.1)
    treat_post_effect = df_effect.query("is_treated == True")
    control_post_effect = df_effect.query("is_treated == False")
    assert all(control_pre_effect["y"] == control_post_effect["y"])
    assert all(treat_pre_effect["y"] * 1.1 == treat_post_effect["y"])


def test_sample_timestamps(evaluator_instance, df_sample):
    df_sampled = evaluator_instance._sample_timestamps(df_sample, 1)
    assert df_sampled["timeframe"].nunique() == 1


@pytest.mark.parametrize("sample_size", [10, 50, 100])
def test_sample_users(evaluator_instance, df_sample, sample_size):
    df_sampled = evaluator_instance._sample_users(df_sample, sample_size)
    assert len(df_sampled) == sample_size


def test_calc_sample_sizes(evaluator_instance):
    sample_sizes = evaluator_instance._calc_sample_sizes()
    assert len(sample_sizes) == evaluator_instance.num_steps
    assert sample_sizes[0] == evaluator_instance.sample_min
    assert sample_sizes[-1] == evaluator_instance.sample_max


# Integration Tests


def test_generate_datasets(evaluator_instance):
    datasets = evaluator_instance._generate_datasets()
    # Assumption: At least one dataset is generated for each combination of mdes, preprocessor, and sample size.
    assert len(datasets) == len(evaluator_instance._preprocessor_names()) * len(
        evaluator_instance._calc_sample_sizes()
    ) * evaluator_instance.num_runs * len(evaluator_instance.mdes)


def test_run(evaluator_instance):
    result = evaluator_instance.run()
    assert "power" in result.get_data().columns


# Edge Cases


def test_invalid_sample_max():
    with pytest.raises(ValueError):
        Simulator(
            pd.DataFrame(), baseline_evaluator="wls", sample_min=1000, sample_max=500
        )


def test_missing_timeframe_column():
    df = pd.DataFrame({"id": range(100), "y": range(100)})
    with pytest.raises(KeyError):
        Simulator(df, baseline_evaluator="wls", sample_timestamps=True)
