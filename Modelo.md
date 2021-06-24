# Paso 1
Descargue los archivos: 
CargarLinescanEnTest.py, 
DCaLinescanCSV.py,
RefactorArchivosCSV.py, 
ModeloMLClasificacion.py, 
ModeloMLSGD.py y mvp.py

# Paso 2
Navegue por Jupyter a la carpeta "03_EY_challenge1". Cliquee el botón de "Upload" de arriba a la derecha.
Cargue los archivos previamente descargados en el paso anterior. 

#Paso 3
Se han generado dos modelos, uno inicial de un solo archivo `mvp.py` y una segunda versión con código modularizado en diferentes Notebooks Jupyter.

Para la segunda versión es necesario ejecutar las Notebooks en el siguiente orden:

1. CargarLinescanEnTest.py 
2. DCaLinescanCSV.py 
3. RefactorArchivosCSV.py
4. ModeloMLClasificacion.py
5. ModeloMLSGD.py (opcional)

Los archivos `DCaLinescanCSV.py` y `RefactorArchivosCSV.py` deberían ejecutarse con los numeros 29, 31 o 39 del dataset  para que el modelo de clasificación funcione correctamente, si prefiere saltarse este paso, simplemente comente las lineas necesarias en los archivos ` ModeloMLClasificacion.py` y `ModeloMLSGD.py`

Finalmente se generará un archivo "Submission 04-06-21_5.csv" el cual es la respuesta a la pregunta inicial
