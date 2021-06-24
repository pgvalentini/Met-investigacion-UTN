%matplotlib inline
import sys
import numpy as np
##!pip install pandas_profiling

import pandas as pd
import geopandas as gpd
from datetime import datetime

from datacube import Datacube
import matplotlib.pyplot as plt

sys.path.append("../scripts")
from dea_plotting import map_shapefile
from dea_spatialtools import xr_rasterize
import pandas_profiling


dc = Datacube(app="Poblar test.csv")


test = pd.read_csv('https://raw.githubusercontent.com/EY-Data-Science-Program/2021-Better-Working-World-Data-Challenge/main/notebooks/03_EY_challenge1/resources/challenge1_test.csv', index_col='id')
print(test.shape)
test.head()

fnames = test.label.unique()
fnames


###Modificacion para poblar el test.csv con los valores correspondientes de linescan

    
for file_stem in fnames:
    
    # cargar linescan data
    src = dc.load(product='linescan', label=file_stem, output_crs='epsg:28355', resolution=(-10,10))
    
    # iterate over the coordinates that are required for testing in the current linescan file
    for idx, ob in test.loc[test.label==file_stem].iterrows():
        result_tf = src.linescan.sel(x=ob.x, y=ob.y, method='nearest').values[0]
      
        test.loc[(test.label==file_stem) & (test.x==ob.x) & (test.y==ob.y), 'linescan'] = result_tf


pandas_profiling.ProfileReport(test)


cols = ['label', 'x','y','dateTimeLocal', 'linescan','target']
test=test[cols]

test.to_csv('test_refactorizado.csv')
