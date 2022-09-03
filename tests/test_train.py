# pylint: disable =import-error
import warnings

import pandas as pd

from pipeline.train import prepare_data

warnings.filterwarnings("ignore")


def test_prepare_data():
    """
    Test the prepare_data function for the continuous_training
    """
    data = pd.read_csv("data/realtor-data.csv")

    features, labels = prepare_data.fn(data, None)

    expected_features = pd.read_csv("data/processed_features.csv")
    expected_labels = pd.read_csv("data/processed_labels.csv", squeeze=True)

    pd.testing.assert_series_equal(labels, expected_labels)
    pd.testing.assert_frame_equal(features, expected_features)
