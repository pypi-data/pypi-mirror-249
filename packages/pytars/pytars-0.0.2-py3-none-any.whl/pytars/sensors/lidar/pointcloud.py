# %%
from dataclasses import dataclass
from typing import Optional

import numpy as np

from pytars.transforms.coordinates import Coordinates
from pytars.utils.timing import datetime64_to_timestamp_seconds


@dataclass
class LidarPointCloud:
    sensor_frame: Coordinates
    transformed_frame: Optional[Coordinates] = None
    intensity: Optional[np.ndarray] = None
    reflectivity: Optional[np.ndarray] = None
    return_num: Optional[np.ndarray] = None
    num_returns: Optional[np.ndarray] = None
    laser_id: Optional[np.ndarray] = None
    frame_num: Optional[np.ndarray] = None
    datetime: Optional[np.ndarray] = None
    lidar_type: str = "default"
    name: str = ""

    @property
    def timestamp_seconds(self):
        """Returns the timestamp in seconds."""
        return datetime64_to_timestamp_seconds(self.datetime)

    def __len__(self):
        return len(self.sensor_frame)

    def __getitem__(self, key) -> "LidarPointCloud":
        sensor_frame = self.sensor_frame[key]

        # rotated frame
        if self.transformed_frame is not None:
            transformed_frame = self.transformed_frame[key]
        else:
            transformed_frame = None

        # intensity
        if self.intensity is not None:
            intensity = self.intensity[key]
        else:
            intensity = None

        # reflectivity
        if self.reflectivity is not None:
            reflectivity = self.reflectivity[key]
        else:
            reflectivity = None

        # return_num
        if self.return_num is not None:
            return_num = self.return_num[key]
        else:
            return_num = None

        # num_returns
        if self.num_returns is not None:
            num_returns = self.num_returns[key]
        else:
            num_returns = None

        # laser_id
        if self.laser_id is not None:
            laser_id = self.laser_id[key]
        else:
            laser_id = None

        # frame_num
        if self.frame_num is not None:
            frame_num = self.frame_num[key]
        else:
            frame_num = None

        # datetime
        if self.datetime is not None:
            datetime = self.datetime[key]
        else:
            datetime = None

        return LidarPointCloud(
            sensor_frame=sensor_frame,
            transformed_frame=transformed_frame,
            intensity=intensity,
            reflectivity=reflectivity,
            return_num=return_num,
            num_returns=num_returns,
            laser_id=laser_id,
            frame_num=frame_num,
            datetime=datetime,
            lidar_type=self.lidar_type,
            name=self.name,
        )
