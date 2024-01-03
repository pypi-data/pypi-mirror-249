from datetime import datetime

import numpy as np

"""
np.datetime64[us] is used instead of datetime:
      - it's more efficient for large arrays
      - it's more convenient for array operations
      - unambiguous units
"""


def extract_datetime64_components(datetime_obj: np.ndarray):
    # Convert to a Python datetime object for easier component extraction
    datetime_py = datetime_obj.astype("datetime64[us]").astype(datetime)

    # Extract components
    year = np.array([x.year for x in datetime_py])
    month = np.array([x.month for x in datetime_py])
    day = np.array([x.day for x in datetime_py])
    hour = np.array([x.hour for x in datetime_py])
    minute = np.array([x.minute for x in datetime_py])
    second = np.array([x.second for x in datetime_py])
    microsecond = np.array([x.microsecond for x in datetime_py])

    return year, month, day, hour, minute, second, microsecond


def timedelta64_to_timestamp_seconds(timedelta_array: np.ndarray) -> np.ndarray:
    """Convert timedelta array to float timestamps in seconds."""
    # Create a copy of the array to avoid modifying the original data
    timestamps = timedelta_array.copy().astype("timedelta64[us]").astype("float64")
    timestamps[np.isnat(timedelta_array)] = np.nan
    return timestamps


def datetime64_to_timestamp_seconds(timedelta_array: np.ndarray) -> np.ndarray:
    """Convert timedelta array to float timestamps in seconds."""
    # Create a copy of the array to avoid modifying the original data
    timestamps = timedelta_array.copy().astype("datetime64[us]").astype("float64")
    timestamps[np.isnat(timedelta_array)] = np.nan
    return timestamps / 1e6


def datetime64_to_timestamps(datetime_array: np.ndarray) -> np.ndarray:
    """Convert datetime array to float timestamps, converting 'NaT' to 'NaN'."""
    # Create a copy of the array to avoid modifying the original data
    timestamps = datetime_array.copy().astype("datetime64[us]").astype("float64")
    timestamps[np.isnat(datetime_array)] = np.nan
    return timestamps


def timestamps_to_datetime64(timestamps: np.ndarray, unit="us") -> np.datetime64:
    """Convert float timestamps back to datetime."""
    return np.datetime64(int(timestamps), unit)


def min_datetime64(datetime_array: np.ndarray) -> np.datetime64:
    """Calculate the minimum datetime."""
    min_timestamp = np.nanmin(datetime64_to_timestamps(datetime_array))
    return timestamps_to_datetime64(min_timestamp)


def mean_datetime64(datetime_array: np.ndarray) -> np.datetime64:
    """Calculate the mean datetime."""
    mean_timestamp = np.nanmean(datetime64_to_timestamps(datetime_array))
    return timestamps_to_datetime64(mean_timestamp)


def max_datetime64(datetime_array: np.ndarray) -> np.datetime64:
    """Calculate the maximum datetime."""
    max_timestamp = np.nanmax(datetime64_to_timestamps(datetime_array))
    return timestamps_to_datetime64(max_timestamp)


def median_datetime64(datetime_array: np.ndarray) -> np.datetime64:
    """Calculate the median datetime."""
    median_timestamp = np.nanmedian(datetime64_to_timestamps(datetime_array))
    return timestamps_to_datetime64(median_timestamp)
