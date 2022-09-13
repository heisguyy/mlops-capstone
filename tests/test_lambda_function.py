# pylint: disable=import-error,duplicate-code
from catboost import CatBoostRegressor
from sklearn.preprocessing import LabelEncoder

from src.lambda_function import download


def test_download():
    """
    Test the download function
    """
    model, encoder = download()

    assert isinstance(model, CatBoostRegressor)
    assert isinstance(encoder, LabelEncoder)
