# %%
from dataclasses import dataclass

import numpy as np


def cart2sph_left_hand_horizon(xyz: np.ndarray, use_degrees: bool = False) -> np.ndarray:
    """Convert cartesian coordinates to spherical coordinates with el=0 when z=0."""
    radius = np.linalg.norm(xyz, axis=1)
    az_radians = np.arctan2(xyz[:, 1], xyz[:, 0])
    dxy = (xyz[:, 0] ** 2 + xyz[:, 1] ** 2) ** 0.5
    el_radians = np.arctan2(xyz[:, 2], dxy)
    if use_degrees:
        return np.stack([np.rad2deg(az_radians), np.rad2deg(el_radians), radius], axis=1)
    else:
        return np.stack([az_radians, el_radians, radius], axis=1)


def sph2cart_left_hand_horizon(az_el_r: np.ndarray, use_degrees: bool = False) -> np.ndarray:
    """Convert spherical coordinates to cartesian coordinates with el=0 when z=0."""
    if use_degrees:
        x = az_el_r[:, 2] * np.cos(np.deg2rad(az_el_r[:, 1])) * np.cos(np.deg2rad(az_el_r[:, 0]))
        y = az_el_r[:, 2] * np.cos(np.deg2rad(az_el_r[:, 1])) * np.sin(np.deg2rad(az_el_r[:, 0]))
        z = az_el_r[:, 2] * np.sin(np.deg2rad(az_el_r[:, 1]))
    else:
        x = az_el_r[:, 2] * np.cos(az_el_r[:, 1]) * np.cos(az_el_r[:, 0])
        y = az_el_r[:, 2] * np.cos(az_el_r[:, 1]) * np.sin(az_el_r[:, 0])
        z = az_el_r[:, 2] * np.sin(az_el_r[:, 1])

    return np.stack([x, y, z], axis=1)


@dataclass
class CoordinateSystem:
    is_cartesian_right_handed: bool = True
    is_spherical_right_handed: bool = False
    is_elevation_0_horizon: bool = True
    azimuth_0_right_hand_math_degrees: float = 90

    def cart2sph(self, xyz: np.ndarray, use_degrees: bool = False) -> np.ndarray:
        """Convert cartesian coordinates to spherical coordinates."""
        if (
            self.is_elevation_0_horizon
            & self.is_cartesian_right_handed
            & ~self.is_spherical_right_handed
            & (self.azimuth_0_right_hand_math_degrees == 90)
        ):
            return cart2sph_left_hand_horizon(xyz, use_degrees=use_degrees)
        else:
            # ENHANCEMENT: generalize this to other coordinate systems
            raise NotImplementedError

    def sph2cart(self, az_el_r: np.ndarray, use_degrees: bool = False) -> np.ndarray:
        """Convert spherical coordinates to cartesian coordinates."""
        if (
            self.is_elevation_0_horizon
            & self.is_cartesian_right_handed
            & ~self.is_spherical_right_handed
            & (self.azimuth_0_right_hand_math_degrees == 90)
        ):
            return sph2cart_left_hand_horizon(az_el_r, use_degrees=use_degrees)
        else:
            # ENHANCEMENT: generalize this to other coordinate systems
            raise NotImplementedError


if __name__ == "__main__":
    test_xyz = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    estimated_sph = cart2sph_left_hand_horizon(test_xyz, use_degrees=True)
    estimated_xyz = sph2cart_left_hand_horizon(estimated_sph, use_degrees=True)
    print(test_xyz)
    print(np.round(estimated_sph, 3))
    print(np.round(estimated_xyz, 3))
    assert np.allclose(test_xyz, estimated_xyz)
