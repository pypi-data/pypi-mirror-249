# %%
from typing import Optional

import numpy as np

from pytars.transforms.cart2sph_coordinate_system import CoordinateSystem
from pytars.transforms.transform import transform_xyz


class Coordinates:
    """Class for storing 3D coordinates in a given coordinate system."""

    def __init__(
        self,
        coordinate_system: CoordinateSystem,
        xyz_meters: Optional[np.ndarray] = None,
        az_el_deg_range_meters: Optional[np.ndarray] = None,
        name="",
        transform_to_current_from_original: np.ndarray = np.eye(4),
    ):
        """Initializes the coordinates."""
        self.coordinate_system = coordinate_system

        if xyz_meters is None and az_el_deg_range_meters is None:
            raise ValueError("Either xyz_meters or az_el_deg_range_meters must be provided")
        elif xyz_meters is None and az_el_deg_range_meters is not None:
            self.az_el_deg_range_meters = az_el_deg_range_meters  # automatically updates xyz_meters
        elif xyz_meters is not None and az_el_deg_range_meters is None:
            self.xyz_meters = xyz_meters  # automatically updates az_el_deg_range_meters
        elif xyz_meters is not None and az_el_deg_range_meters is not None:
            self.xyz_meters = xyz_meters
            self.az_el_deg_range_meters = az_el_deg_range_meters

        self.transform_to_current_from_original = transform_to_current_from_original
        self.name = name

    def __len__(self):
        return len(self.xyz_meters)

    @property
    def xyz_meters(self) -> np.ndarray:
        return self._xyz_meters

    @xyz_meters.setter
    def xyz_meters(self, xyz_meters: np.ndarray):
        """Sets the xyz coordinates + updates az_el_deg_range_meters."""
        self._xyz_meters = xyz_meters
        self._az_el_deg_range_meters = self.coordinate_system.cart2sph(xyz_meters, True)

    @property
    def az_el_deg_range_meters(self) -> np.ndarray:
        return self._az_el_deg_range_meters

    @az_el_deg_range_meters.setter
    def az_el_deg_range_meters(self, az_el_deg_range_meters: np.ndarray):
        """Sets the azimuth, elevation, and range of the coordinates + updates xyz_meters."""
        self._az_el_deg_range_meters = az_el_deg_range_meters
        self._xyz_meters = self.coordinate_system.sph2cart(az_el_deg_range_meters, True)

    def apply_transform(self, new_transform_to_current_from_original: np.ndarray):
        """Transform 3D points based on 4x4 rotation matrix."""
        self.xyz_meters = transform_xyz(self.xyz_meters, new_transform_to_current_from_original)
        self.transform_to_current_from_original @= new_transform_to_current_from_original

    def transformed(self, new_transform_to_current_from_original: np.ndarray) -> "Coordinates":
        """Transform 3D points based on 4x4 rotation matrix."""
        new_Coordinates = self.copy()
        new_Coordinates.apply_transform(new_transform_to_current_from_original)
        return new_Coordinates

    def copy(self) -> "Coordinates":
        """Returns a copy of the current coordinates."""
        return Coordinates(
            xyz_meters=self.xyz_meters,
            coordinate_system=self.coordinate_system,
            az_el_deg_range_meters=self.az_el_deg_range_meters,
            name=self.name,
            transform_to_current_from_original=self.transform_to_current_from_original,
        )

    def get_origin(self) -> np.ndarray:
        """Returns the origin of the current coordinate system."""
        return self.transform_to_current_from_original[:3, 3]

    def __getitem__(self, key):
        # Extract the relevant subset of xyz_meters and az_el_deg_range_meters
        new_xyz_meters = self._xyz_meters[key]
        new_az_el_deg_range_meters = self._az_el_deg_range_meters[key]

        # Create a new instance of the Coordinates class with the extracted data
        return Coordinates(
            xyz_meters=new_xyz_meters,
            coordinate_system=self.coordinate_system,
            az_el_deg_range_meters=new_az_el_deg_range_meters,
            name=self.name,
            transform_to_current_from_original=self.transform_to_current_from_original,
        )

    # helper properties
    @property
    def x_meters(self) -> np.ndarray:
        return self.xyz_meters[:, 0]

    @property
    def y_meters(self) -> np.ndarray:
        return self.xyz_meters[:, 1]

    @property
    def z_meters(self) -> np.ndarray:
        return self.xyz_meters[:, 2]

    @property
    def azimuth_degrees(self) -> np.ndarray:
        return self.az_el_deg_range_meters[:, 0]

    @property
    def elevation_degrees(self) -> np.ndarray:
        return self.az_el_deg_range_meters[:, 1]

    @property
    def range_meters(self) -> np.ndarray:
        return self.az_el_deg_range_meters[:, 2]
