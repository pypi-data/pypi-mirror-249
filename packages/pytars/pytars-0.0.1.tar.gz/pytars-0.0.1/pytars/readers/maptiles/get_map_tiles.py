# %%
import logging
from io import BytesIO
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from tqdm import tqdm

from pytars.readers.maptiles.tile_servers import TileServer, TileServerType


class MapData:
    """A class to hold a map tile and its metadata."""

    def __init__(
        self,
        raw_rgb: np.ndarray,
        extent_lon_lat: Tuple[float, float, float, float],
        x_y_min_max: Tuple[int, int, int, int],
        zoom_level: int,
        tile_server: TileServer,
    ):
        self._raw_rgb = raw_rgb
        self.extent_lon_lat = extent_lon_lat
        self.x_y_min_max = x_y_min_max
        self.zoom_level = zoom_level
        self.tile_server = tile_server

    @property
    def lat_lon_vector(self):
        """Returns the lat lon vector."""
        lat_vector = np.linspace(
            self.extent_lon_lat[3], self.extent_lon_lat[2], self._raw_rgb.shape[0]
        )
        lon_vector = np.linspace(
            self.extent_lon_lat[0], self.extent_lon_lat[1], self._raw_rgb.shape[1]
        )
        return lat_vector, lon_vector

    @property
    def rgb(self):
        """Returns the rgb image."""
        if self.tile_server.tiles_type != "rgb":
            raise ValueError("This tile is not an rgb tile")
        return self._raw_rgb

    @property
    def elevation_meters(self):
        """Returns the elevation in meters."""
        if self.tile_server.tiles_type != "elevation":
            raise ValueError("This tile is not an elevation tile")
        return convert_elevation_tile_to_meters(self._raw_rgb)


def convert_latlon_to_tile(lat_deg: float, lon_deg: float, z_level: int) -> Tuple[float, float]:
    """Converts lat lon to tile coordinates for a given zoom"""
    lat_rad = np.deg2rad(lat_deg)
    n = 2.0**z_level
    x_tile = (lon_deg + 180.0) / 360.0 * n
    y_tile = (1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n
    return x_tile, y_tile


def convert_tile_to_latlon(x_tile: int, y_tile: int, z_level: int) -> Tuple[float, float]:
    """Converts tile coordinates to lat lon for a given zoom"""
    n = 2.0**z_level
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * y_tile / n)))
    lat_deg = np.rad2deg(lat_rad)
    return lat_deg, lon_deg


def convert_elevation_tile_to_meters(rgb_image: np.ndarray) -> np.ndarray:
    """Converts a elevation tile to meters"""
    return rgb_image[:, :, 0] * 256 + rgb_image[:, :, 1] + rgb_image[:, :, 2] / 256 - 32768


def download_map_tile_from_server(
    x: int,
    y: int,
    zoom_level: int,
    server: TileServer = TileServerType.ARCGIS.value,
) -> np.ndarray:
    """Get a map tile from a server."""
    logging.debug(f"Downloading tile: {x}, {y}, {zoom_level}")
    # check that x and y an dzoom level are int or np int
    if not isinstance(x, (int, np.int64, np.int32)):
        raise ValueError(f"x must be an integer - is actually a {type(x)} val = ({x})")
    if not isinstance(y, (int, np.int64, np.int32)):
        raise ValueError(f"y must be an integer - is actually a {type(y)} val = ({y})")
    if not isinstance(zoom_level, (int, np.int64, np.int32)):
        raise ValueError(
            f"zoom_level must be an integer - is actually a {type(zoom_level)} val = ({zoom_level})"
        )

    # check that zoom level is valid
    if not server.zoom_level_range[0] <= zoom_level <= server.zoom_level_range[1]:
        raise ValueError(
            f"Zoom level must be between {server.zoom_level_range[0]} and {server.zoom_level_range[1]}"
        )
    # Define a mapping from characters to the corresponding values
    coord_map = {"X": x, "Y": y, "Z": zoom_level}

    # Validate the server_order
    if not all(char in coord_map for char in server.server_order):
        raise ValueError("Server order must only contain characters 'X', 'Y', and 'Z'")

    # Use the server_order to arrange the coordinates
    ordered_coords = [str(coord_map[char]) for char in server.server_order]

    # Create the image path
    image_path = "/".join(ordered_coords) + server.server_extension

    # check if url exists locally
    cache_path = server.cache_path() / image_path
    if cache_path.exists():
        return np.array(Image.open(cache_path))

    # check if the url is valid
    image_url = server.url + image_path

    # request image with timeout
    is_valid = requests.get(image_url, timeout=5).status_code == 200

    # read image
    raw_image_response = requests.get(image_url, timeout=5)

    # check if it's a valid image
    is_valid = raw_image_response.status_code == 200
    if not is_valid:
        raise ValueError(f"Image doesnt exist: {image_url}")

    # return numpy array
    image_array = np.array(Image.open(BytesIO(raw_image_response.content)))
    # save image to cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image_array).save(cache_path)
    return image_array


def download_multiple_map_tiles_from_server(
    x_min_max: Tuple[int, int],
    y_min_max: Tuple[int, int],
    zoom_level: int,
    server: TileServer,
    show_tqdm: bool = True,
    max_download_tiles: int = 100,
):
    """Get multiple map tilea from a server."""
    # check to make sure not downloading too much
    num_x = x_min_max[1] - x_min_max[0] + 1
    num_y = y_min_max[1] - y_min_max[0] + 1
    num_to_download = num_x * num_y
    if num_to_download > max_download_tiles:
        raise ValueError(
            "Whoa there partner, thats a lot of data. "
            + "If you are really really sure, "
            + "set max_download_tiles to override this error."
        )
    # preallocate array
    raw_rgb = np.zeros((256 * num_y, 256 * num_x, 3), dtype=np.uint8)
    # download tiles
    if show_tqdm:
        pbar = tqdm(total=num_to_download)
    for i_x, x in enumerate(np.arange(x_min_max[0], x_min_max[1] + 1)):
        for i_y, y in enumerate(np.arange(y_min_max[0], y_min_max[1] + 1)):
            if show_tqdm:
                pbar.update(1)
            i_raw_rgb = download_map_tile_from_server(x, y, zoom_level, server)
            raw_rgb[i_y * 256 : (i_y + 1) * 256, i_x * 256 : (i_x + 1) * 256, :] = i_raw_rgb
    return raw_rgb


def get_map_data_from_xy(
    x: Union[int, Tuple[int, int]],
    y: Union[int, Tuple[int, int]],
    zoom_level: int,
    server: TileServer = TileServerType.ARCGIS.value,
) -> MapData:
    """Get a rgb tile from the arcgis server"""

    # Download rgb data
    if isinstance(x, int) and isinstance(y, int):
        raw_rgb = download_map_tile_from_server(x, y, zoom_level, server)
        lat_lon_upper_left = convert_tile_to_latlon(x, y, zoom_level)
        lat_lon_lower_right = convert_tile_to_latlon(x + 1, y + 1, zoom_level)
        xy_min_max = (x, x, y, y)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == 2 and len(y) == 2:
        raw_rgb = download_multiple_map_tiles_from_server(x, y, zoom_level, server)
        lat_lon_upper_left = convert_tile_to_latlon(x[0], y[0], zoom_level)
        lat_lon_lower_right = convert_tile_to_latlon(x[-1] + 1, y[-1] + 1, zoom_level)
        xy_min_max = (x[0], x[-1], y[0], y[-1])
    else:
        raise ValueError("x and y must be either both int or both tuples of length 2")
    # calculate lat lon extent
    extent_lon_lat = (
        lat_lon_upper_left[1],
        lat_lon_lower_right[1],
        lat_lon_lower_right[0],
        lat_lon_upper_left[0],
    )
    # return MapData
    return MapData(
        raw_rgb,
        extent_lon_lat,
        xy_min_max,
        zoom_level,
        server,
    )


def get_map_data_from_lat_lon(
    center_latitude_deg: float,
    center_longitude_deg: float,
    zoom_level: int,
    server: TileServer = TileServerType.ARCGIS.value,
    image_buffer_x: int = 1,
    image_buffer_y: int = 1,
) -> MapData:
    """Get a map data from server based on lat lon."""
    center_x, center_y = convert_latlon_to_tile(
        center_latitude_deg, center_longitude_deg, zoom_level
    )

    x_extent = (int(center_x - image_buffer_x), int(center_x + image_buffer_x))
    y_extent = (int(center_y - image_buffer_y), int(center_y + image_buffer_y))

    return get_map_data_from_xy(x_extent, y_extent, zoom_level, server)


if __name__ == "__main__":
    # setup logging
    # logging.basicConfig(level=logging.DEBUG)
    IMAGE_BUFFER_X = 3
    IMAGE_BUFFER_Y = 2
    Z_LAYER = 15
    # SF
    CENTER_LAT = 37.8
    CENTER_LON = -122.4194

    rgb_data = get_map_data_from_lat_lon(
        CENTER_LAT, CENTER_LON, Z_LAYER, TileServerType.ARCGIS.value, IMAGE_BUFFER_X, IMAGE_BUFFER_Y
    )
    elevation_data = get_map_data_from_lat_lon(
        CENTER_LAT,
        CENTER_LON,
        Z_LAYER,
        TileServerType.TERRARIUM.value,
        IMAGE_BUFFER_X,
        IMAGE_BUFFER_Y,
    )

    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    axs[0].imshow(rgb_data.rgb, extent=rgb_data.extent_lon_lat)
    axs[1].imshow(
        elevation_data.elevation_meters, cmap="terrain", extent=elevation_data.extent_lon_lat
    )
    lat_vector, lon_vector = elevation_data.lat_lon_vector
    axs[0].contour(lon_vector, lat_vector, elevation_data.elevation_meters, [0], colors="m")
    axs[1].contour(lon_vector, lat_vector, elevation_data.elevation_meters, [0], colors="k")
