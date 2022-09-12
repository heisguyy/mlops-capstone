# pylint: disable =import-error
import warnings

import pandas as pd

from pipeline.train import get_data, prepare_data

warnings.filterwarnings("ignore")


def test_get_prepare_data():
    """
    Test the prepare_data function for the continuous_training
    """
    data = get_data.fn()

    features, labels = prepare_data.fn(data, None)

    expected_features = pd.read_csv("data/processed_features.csv")

    assert features.columns.to_list() == expected_features.columns.to_list()
    assert not features.isna().any().any()
    assert not labels.isna().any().any()
