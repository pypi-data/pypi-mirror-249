import lightgbm as lgb

from sktime.forecasting.compose import make_reduction, ForecastingPipeline
from sktime.forecasting.naive import NaiveForecaster
from sktime.transformations.series.date import DateTimeFeatures
from sktime.transformations.series.summarize import WindowSummarizer

from training_pipeline import transformers


def build_model(config: dict):
    """
    Build an Sktime model using the given config.

    It supports defaults for windowing the following parameters:
    - lag: list(range(1, 504 + 1))
    - mean: [[1, 168], [1, 336], [1, 504]]
    - std: [[1, 168], [1, 336], [1, 504]]
    """

    lag = config.pop(
        "forecaster_transformers__window_summarizer__lag_feature__lag",
        list(range(1, 21 + 1)),
    )
    mean = config.pop(
        "forecaster_transformers__window_summarizer__lag_feature__mean",
        [[1, 7], [1, 14], [1, 21]],
    )
    std = config.pop(
        "forecaster_transformers__window_summarizer__lag_feature__std",
        [[1, 7], [1, 14], [1, 21]],
    )
    n_jobs = config.pop("forecaster_transformers__window_summarizer__n_jobs", 1)
    window_summarizer = WindowSummarizer(
        **{"lag_feature": {"lag": lag, "mean": mean, "std": std}},
        n_jobs=n_jobs,
    )

    regressor = lgb.LGBMRegressor()
    forecaster = make_reduction(
        regressor,
        transformers=[window_summarizer],
        strategy="recursive",
        pooling="global",
        window_length=None,
    )

    pipe = ForecastingPipeline(
        steps=[
            ("attach_area_and_consumer_type", transformers.AttachAreaConsumerType()),
            (
                "daily_season",
                DateTimeFeatures(
                    #manual_selection=["day_of_week", "hour_of_day"],
                    #manual_selection=["day_of_week"],
                    keep_original_columns=True,
                ),
            ),
            ("forecaster", forecaster),
        ]
    )
    pipe = pipe.set_params(**config)

    return pipe


def build_baseline_model(seasonal_periodicity: int):
    """Builds a naive forecaster baseline model using Sktime that predicts the last value given a seasonal periodicity."""

    return NaiveForecaster(sp=seasonal_periodicity)
