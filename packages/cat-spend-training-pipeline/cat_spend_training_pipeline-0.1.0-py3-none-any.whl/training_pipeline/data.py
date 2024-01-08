from typing import Tuple
import hopsworks
import pandas as pd
import wandb

#from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.split import temporal_train_test_split

from training_pipeline.utils import init_wandb_run
from training_pipeline.settings import SETTINGS

from training_pipeline import utils
logger = utils.get_logger(__name__)

def load_dataset_from_feature_store(
    feature_view_version: int, training_dataset_version: int, fh: int = 7
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load features from feature store.

    Args:
        feature_view_version (int): feature store feature view version to load data from
        training_dataset_version (int): feature store training dataset version to load data from
        fh (int, optional): Forecast horizon. Defaults to 24.

    Returns:
        Train and test splits loaded from the feature store as pandas dataframes.
    """

    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project=SETTINGS["FS_PROJECT_NAME"]
    )
    fs = project.get_feature_store()

    with init_wandb_run(
        name="load_training_data", job_type="load_feature_view", group="dataset"
    ) as run:
        feature_view = fs.get_feature_view(
            name="category_spend_breakfast_frat_view", version=feature_view_version
        )
        data, _ = feature_view.get_training_data(
            training_dataset_version=training_dataset_version
        )

        fv_metadata = feature_view.to_dict()
        fv_metadata["query"] = fv_metadata["query"].to_string()
        fv_metadata["features"] = [f.name for f in fv_metadata["features"]]
        fv_metadata["link"] = feature_view._feature_view_engine._get_feature_view_url(
            feature_view
        )
        fv_metadata["feature_view_version"] = feature_view_version
        fv_metadata["training_dataset_version"] = training_dataset_version

        raw_data_at = wandb.Artifact(
            name="category_spend_breakfast_frat_view",
            type="feature_view",
            metadata=fv_metadata,
        )
        run.log_artifact(raw_data_at)

        run.finish()

    with init_wandb_run(
        name="train_test_split", job_type="prepare_dataset", group="dataset"
    ) as run:
        run.use_artifact("category_spend_breakfast_frat_view:latest")

        y_train, y_test, X_train, X_test = prepare_data(data, fh=fh)

        for split in ["train", "test"]:
            split_X = locals()[f"X_{split}"]
            split_y = locals()[f"y_{split}"]

            split_metadata = {
                "timespan": [
                    split_X.index.get_level_values(-1).min(),
                    split_X.index.get_level_values(-1).max(),
                ],
                "dataset_size": len(split_X),
                "num_cod_categories": len(split_X.index.get_level_values(0).unique()),
                "num_categories": len(split_X.index.get_level_values(1).unique()),
                "num_store_names": len(split_X.index.get_level_values(2).unique()),
                "y_features": split_y.columns.tolist(),
                "X_features": split_X.columns.tolist(),
            }
            artifact = wandb.Artifact(
                name=f"split_{split}",
                type="split",
                metadata=split_metadata,
            )
            run.log_artifact(artifact)

        run.finish()

    return y_train, y_test, X_train, X_test


def prepare_data(
    data: pd.DataFrame, target: str = "spend", fh: int = 7
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Structure the data for training:
    - Set the index as is required by sktime.
    - Prepare exogenous variables.
    - Prepare the time series to be forecasted.
    - Split the data into train and test sets.
    """
    
    logger.info(f"MIN week_end_date... {data['week_end_date'].min()}")
    logger.info(f"MAX week_end_date... {data['week_end_date'].max()}")
    logger.info(f"forecast horizon... {fh}")

    # Set the index as is required by sktime.
    data["week_end_date"] = pd.PeriodIndex(data["week_end_date"], freq="D")
    data = data.set_index(["cod_category", "category", "store_name", "week_end_date"]).sort_index()
    
    # Prepare exogenous variables.
    X = data.drop(columns=[target])
    # Prepare the time series to be forecasted.
    y = data[[target]]

    y_train, y_test, X_train, X_test = temporal_train_test_split(y, X, test_size=fh)

    return y_train, y_test, X_train, X_test
