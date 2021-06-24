import os
import sys
import datacube
from datacube.helpers import write_geotiff
import numpy as np
import xarray as xr
from shapely.geometry import Point
import matplotlib as plt
import glob
import rasterio
from rasterio.merge import merge
from rasterio.plot import show

sys.path.append('../Scripts')
from dea_bandindices import calculate_indices




