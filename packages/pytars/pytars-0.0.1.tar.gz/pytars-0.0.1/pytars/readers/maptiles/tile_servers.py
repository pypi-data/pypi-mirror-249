# %%
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple

from pytars.utils.get_project_path import get_temp_path


@dataclass
class TileServer:
    url: str
    server_order: str
    server_extension: str
    cache_name: str
    tiles_type: str
    zoom_level_range: Tuple[int, int]

    def cache_path(self) -> Path:
        return get_temp_path() / "map_tile_cache" / self.cache_name


class TileServerType(Enum):
    ARCGIS = TileServer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/",
        server_order="ZYX",
        server_extension=".png",
        cache_name="arcgis",
        tiles_type="rgb",
        zoom_level_range=(0, 20),
    )
    TERRARIUM = TileServer(
        url="https://s3.amazonaws.com/elevation-tiles-prod/terrarium/",
        server_order="ZXY",
        server_extension=".png",
        cache_name="terrarium",
        tiles_type="elevation",
        zoom_level_range=(0, 15),
    )
