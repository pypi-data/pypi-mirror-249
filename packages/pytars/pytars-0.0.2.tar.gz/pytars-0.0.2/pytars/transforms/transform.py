import numpy as np
from scipy.spatial.transform import Rotation as R


def transform_xyz(points_xyz: np.ndarray, extrinsic_4x4: np.ndarray) -> np.ndarray:
    """Transform 3D points based on 4x4 rotation matrix."""
    points_xyz_homogeneous = np.concatenate([points_xyz, np.ones((points_xyz.shape[0], 1))], axis=1)
    rotated_xyz = points_xyz_homogeneous @ extrinsic_4x4
    return rotated_xyz[:, :3]


def create_rotation_matrix_4x4(tx, ty, tz, roll_deg, pitch_deg, yaw_deg):
    """Creates a 4x4 rotation matrix from the given translation and rotation."""
    r = R.from_euler("xyz", [roll_deg, pitch_deg, yaw_deg], degrees=True)
    rotation_matrix = r.as_matrix()
    translation_matrix = np.eye(4)
    translation_matrix[:3, 3] = np.array([tx, ty, tz])
    return translation_matrix @ rotation_matrix
