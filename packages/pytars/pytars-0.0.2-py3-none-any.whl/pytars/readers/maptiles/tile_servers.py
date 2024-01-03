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
    do_cache: bool = False

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
    """
    * ArcticDEM terrain data DEM(s) were created from DigitalGlobe, Inc., imagery and
    funded under National Science Foundation awards 1043681, 1559691, and 1542736;
    * Australia terrain data © Commonwealth of Australia (Geoscience Australia) 2017;
    * Austria terrain data © offene Daten Österreichs – Digitales Geländemodell (DGM)
    Österreich;
    * Canada terrain data contains information licensed under the Open Government
    Licence – Canada;
    * Europe terrain data produced using Copernicus data and information funded by the
    European Union - EU-DEM layers;
    * Global ETOPO1 terrain data U.S. National Oceanic and Atmospheric Administration
    * Mexico terrain data source: INEGI, Continental relief, 2016;
    * New Zealand terrain data Copyright 2011 Crown copyright (c) Land Information New
    Zealand and the New Zealand Government (All rights reserved);
    * Norway terrain data © Kartverket;
    * United Kingdom terrain data © Environment Agency copyright and/or database right
    2015. All rights reserved;
    * United States 3DEP (formerly NED) and global GMTED2010 and SRTM terrain data
    courtesy of the U.S. Geological Survey.
    """
