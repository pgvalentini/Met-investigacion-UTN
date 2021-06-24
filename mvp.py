
# Importo librerías para trabajar con datos geográficos
import matplotlib.pyplot as plt
from datacube import Datacube
from datetime import datetime
import geopandas as gpd
import numpy as np
import pandas as pd

# Analisis exploratorio
url = 'https://raw.githubusercontent.com/EY-Data-Science-Program/2021-Better-Working-World-Data-Challenge/main/notebooks/03_EY_challenge1/resources/challenge1_train.csv'

df = pd.read_csv(url)

print(df.head())

# Instancio un datacube
dc = Datacube(app="Aplicacion_Datacube")

dataset_de_barrido_lineal = dc.find_datasets(product='linescan')
dataset_de_barrido_lineal = sorted(
    dataset_de_barrido_lineal, key=lambda ds: (ds.center_time, ds.id))

muestra = dataset_de_barrido_lineal[0]

print(muestra)
print(muestra.metadata_doc['label'])

print(
    f'\nCantidad de datasets de barrido lineal: {len(dataset_de_barrido_lineal)}')
# En dataset_de_barrido_lineal hay metadatos, para cargar cada metadato se usa este código a continuación
ds = dc.load(product='linescan',
             id=dataset_de_barrido_lineal[23].id, output_crs='epsg:28355', resolution=(-10, 10))
print(ds)
# Representación gráfica
ds.linescan.plot()

# Cargamos la imagen con los polígonos del mapa de fuego
vector_poligonos = 'recursos/fire_boundaries.shp'
gdf = gpd.read_file(url)
print('Numero de objetos en el geodataframe: ' + str(len(gdf)))
gdf.head().T


atributo_col = 'SourceName'
map_shapefile(gdf, atributo=atributo_col, fillOpacity=0.2,
              color="yellow", fillColor="red", default_zoom=8)

# Correspondencia directa de nombres (cuando el polígono está compuesto de una sola imagen)

# Formato en barrido lineal
print(dataset_de_barrido_lineal[23].metadata_doc['label'])
print(gdf.SourceName[0])  # Formato en dataset polígonos

# Este codigo investiga los poligonos compuestos por más de una imagen

composicion = gdf[gdf.SourceName.str.upper(
).str.contains(",|&|(COMPOSITE)", na=False)]

print(f"Total composición polígonos: {len(composicion)}")

composicion.SourceName.head()

composicion.SourceName.unique()


# Esta función es para unificar los diferentes formatos entre el dataset de polígonos y el de barridos lineales
def limpiar_nombre(nombre):
    if nombre is None:
        res = None
    else:
        if nombre.upper()[-4::] == ".JPG":
            res = nombre.upper()[:-4].replace(' ', '_')
        else:
            res = nombre.upper().replace(' ', '_')
    return res


string_de_prueba = 'aberfeldy west 200 p1_201901260955_mga94_55.jpg'
string_de_prueba_composicion = 'Composite wallhalla 397,398 & 401 20190225 (1311 to 1342hrs)'
print(limpiar_nombre(string_de_prueba))
print(limpiar_nombre(string_de_prueba_composicion))

gdf['SourceNameClean'] = gdf.apply(
    lambda row: limpiar_nombre(row.SourceName), axis=1)
gdf.dtUTC = gdf.apply(lambda row: datetime.strptime(
    row.dtUTC, '%Y-%m-%d %H:%M:%S'), axis=1)
gdf.dtLocal = gdf.apply(lambda row: datetime.strptime(
    row.dtLocal, '%Y-%m-%d %H:%M:%S'), axis=1)
gdf.head().T

url_test = 'https://raw.githubusercontent.com/EY-Data-Science-Program/2021-Better-Working-World-Data-Challenge/main/notebooks/03_EY_challenge1/resources/challenge1_test.csv'
test = pd.read_csv(url_test)
print(test.shape)
test.head()

nombres_de_vuelos = test.label.unique()
nombres_de_vuelos


# Este código compara el valor de la variable linescan contra el umbral, de manera de asignar valores de 1 cuando está en curso el incendio y 0 cuando no hay fuego
# para cada par de coordenadas del dataset de test

umbral = 60

for etiquetas in nombres_de_vuelos:

    # Carga los datos de escaneo lineal
    fuente = dc.load(product='linescan', label=etiquetas,
                  output_crs='epsg:28355', resolution=(-10, 10))

    # Crea una máscara utilizando el proceso que desarrollamos anteriormente. Para este ejemplo, simplemente estableceremos el umbral de cada escaneo lineal
    mascara = fuente.linescan > umbral

    # Itera sobre las coordenadas que se requieren para la prueba en el archivo de escaneo lineal
    for idx, ob in test.loc[test.label == etiquetas].iterrows():
        resultado_tf = mascara.sel(x=ob.x, y=ob.y, method='nearest').values[0]
        resultado_10 = int(resultado_tf == True)
        test.loc[(test.label == etiquetas) & (test.x == ob.x)
                 & (test.y == ob.y), 'target'] = resultado_10

test.target.value_counts()

test.to_csv('Archivo.csv', columns=['target'])
test.head()

# Esta resolución tiene un score de 0.49746 en la predicción.
