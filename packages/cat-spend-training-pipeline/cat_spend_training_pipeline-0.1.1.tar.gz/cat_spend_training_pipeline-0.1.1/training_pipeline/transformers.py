from sktime.transformations.base import BaseTransformer
#from sktime.transformations.compose import CORE_MTYPES


from training_pipeline import utils
logger = utils.get_logger(__name__)

class AttachAreaConsumerType(BaseTransformer):
    """Transformer used to extract the area and consumer type from the index to the input data."""

    _tags = {
        "capability:inverse_transform": True,  # can the transformer inverse transform?
        "univariate-only": False,  # can the transformer handle multivariate X?
        #"X_inner_mtype": CORE_MTYPES,  # which mtypes do _fit/_predict support for X?
        #"X_inner_mtype": ["pd-multiindex", "pd_multiindex_hier"],  # which mtypes do _fit/_predict support for X?
        "X_inner_mtype": "pd_multiindex_hier",  # which mtypes do _fit/_predict support for X?
        # this can be a Panel mtype even if transform-input is Series, vectorized
        "y_inner_mtype": "None",  # which mtypes do _fit/_predict support for y?
        "fit_is_empty": True,  # is fit empty and can be skipped? Yes = True
        "transform-returns-same-time-index": True,
        # does transform return have the same time index as input X
        "handles-missing-data": True,  # can estimator handle missing data?
    }

    def _transform(self, X, y=None):
        #X["cod_category_exog"] = X.index.get_level_values(0)
        X["category_exog"] = X.index.get_level_values(0)
        X["store_name_exog"] = X.index.get_level_values(1)

        #logger.info("****************** LOG DO TRANSFORMER X ******************")
        #logger.info(X.info())
        #logger.info(X.head())
        #logger.info(X.shape)


        return X

    def _inverse_transform(self, X, y=None):
        X = X.drop(columns=["category_exog", "store_name_exog"])

        return X
