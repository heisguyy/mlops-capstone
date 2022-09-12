# pylint: disable=too-few-public-methods
import os
from typing import Optional


def load_from_env(env_var_name: str, default: Optional[str] = None) -> Optional[str]:
    """Loads environment variables.

    Args:
        env_var_name (str): key of environment variable
        default (Optional[str], optional): Value to use in case no value
                        is defined in the environment. Defaults to None.

    Returns:
        Optional[str]: Environment variable
    """
    return os.environ.get(env_var_name, default)


def load_from_env_to_int(env_var_name: str, default: int) -> int:
    """Loads environment variable and converts it to int.

    Args:
        env_var_name (str): key of environment variable
        default (int): default integer to use in case none is defined.

    Returns:
        int: Integer environment variable
    """
    try:
        return int(load_from_env(env_var_name) or default)
    except Exception:  # pylint: disable=broad-except
        print("Could not load environment variable")
        return default


class Configuration:
    # Batch size ... default to 100, do not send until batch size is reached
    # batch_size: int = load_from_env_to_int("MODEL_MONITOR_BATCH_SIZE", 100)

    # # Batch window ... wait for this long before sending, default to 1 minute
    # batch_window: float = load_from_env_to_int("MODEL_MONITOR_BATCH_WINDOW", 60000) / 1000

    # S3 bucket ... for S3 Handler, write data to this bucket, optional
    s3_bucket: Optional[str] = load_from_env("MODEL_MONITOR_S3_BUCKET")

    is_test: Optional[str] = load_from_env("IS_TEST")
