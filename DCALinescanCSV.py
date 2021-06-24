%matplotlib inline
import sys
import numpy as np         
import pandas as pd        
import geopandas as gpd    
from datetime import datetime
import xarray as xr        

from datacube import Datacube 
import matplotlib.pyplot as plt

sys.path.append("../scripts")
from dea_plotting import map_shapefile
from dea_spatialtools import xr_rasterize

dc = Datacube(app="DatacubeALinescanNroX")


#En la siguiente línea escribimos el linescan que queremos descargar
num_linescan= 38

linescan_datasets = dc.find_datasets(product='linescan')
linescan_datasets = sorted(linescan_datasets, key = lambda ds: (ds.center_time, ds.id))

ds = dc.load(product='linescan', id=linescan_datasets[num_linescan].id, output_crs='epsg:28355', resolution=(-100,100))
print(ds)  

archivo_vector = 'resources/fire_boundaries.shp'
gdf = gpd.read_file(archivo_vector)

def limpiar_nombre(nombre):
    if nombre is None:
        res = None
    else:
        if nombre.upper()[-4::] == ".JPG":
            res = nombre.upper()[:-4].replace(' ','_')
        else:
            res = nombre.upper().replace(' ','_')
    return res

test_string = 'aberfeldy west 200 p1_201901260955_mga94_55.jpg'
test_string_composicion = 'Composite wallhalla 397,398 & 401 20190225 (1311 to 1342hrs)'
print(limpiar_nombre(test_string))

gdf['SourceNameClean'] = gdf.apply(lambda row: limpiar_nombre(row.SourceName), axis=1)
gdf.dtUTC = gdf.apply(lambda row: datetime.strptime(row.dtUTC, '%Y-%m-%d %H:%M:%S'), axis=1)
gdf.dtLocal = gdf.apply(lambda row: datetime.strptime(row.dtLocal, '%Y-%m-%d %H:%M:%S'), axis=1)
gdf.head().T

gdf.Type.value_counts()


fnombre = linescan_datasets[num_linescan].metadata_doc['label']
print(fnombre)
print(f"There are {sum(gdf.SourceNameClean == fnombre)} polygons for linescan {fnombre}")

ob = gdf.loc[gdf.SourceNameClean == fnombre]

src = dc.load(product='linescan', id=linescan_datasets[num_linescan].id, output_crs='epsg:28355', resolution=(-100,100))


tgt = xr_rasterize(gdf=ob, da=src)

tgt.name='target'

unidosOut=xr.merge([src, tgt],join='outer' )

unidosOut=unidosOut.drop('spatial_ref')

unidosOut=unidosOut.drop('time')

miDF=unidosOut.to_dataframe()

miDF.linescan.mean()


miDF['label']= fnombre

fecha=fnombre[-21:]

dia= fecha[6:8]
print(dia)

mes= fecha[4:6]
print(mes)

anio= fecha[0:4]
print(anio)

hora = fecha[8:10]
print(hora)

min = fecha[10:12]
print(min)

fechaHoraLocal= f'{dia}/{mes}/{anio} {hora}:{min}'
print(fechaHoraLocal)

miDF['dateTimeLocal']=fechaHoraLocal

# Crear el csv
nombrearchivo= f'Linescan_nro {num_linescan} label {fnombre}.csv'
miDF.to_csv(nombrearchivo, line_terminator='\n')

print(f'ok {num_linescan}')























