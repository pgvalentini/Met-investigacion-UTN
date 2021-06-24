# Sobre el proyecto:
Más información en [Leeme.md](https://github.com/UTN-FRM-TUP/Grupo-I-TT/blob/master/LEEME.md)

# Configuración del entorno local.

Cube in a Box usa Docker para lanzar un entorno completo de Open Data Cube (que es la base desde donde obtenemos el dataset). Una vez ejecutado, se podrá acceder al entorno interactivo de Python utilizando Jupyter en el navegador, preindexado con datos de satélite e imágenes de barrido lineal. 

# Requerimientos:
* [Docker](https://docker.com/) instalado y ejecutándose en su computadora.
* [Docker Compose](https://docs.docker.com/compose/install/) para coordinar varios contenedores de Docker.
* Una terminal para ejecutar los comandos de configuración. En MacOS puede usar Terminal.app, en Linux probablemente sepa qué hacer.
* [Git](https://git-scm.com/). También es necesario tenerlo instalado para clonar el repositorio.
* Alternativamente, puede [descargar un zip de este repositorio](https://github.com/EY-Data-Science-Program/2021-Better-Working-World-Data-Challenge/archive/main.zip).

# Ejecución de un Datacube local

Una vez que se hayan cumplido con los requisitos anteriores, ¡estará listo para lanzar su propio datacube abierto personal!

Abra una terminal y ejecute los siguientes comandos:
## Paso 1: obtener el código 

Si usa Windows, puede crear una nueva carpeta en `C:/Usuarios/usuario/dockerfiles/` como `cube-in-a-box` y abrir una terminal de Windows Powershell dentro de ella y luego clonar el repositorio.

Si está usando git, puede clonar el repositorio usando: 

`https://github.com/EY-Data-Science-Program/2021-Better-Working-World-Data-Challenge.git`

Alternativamente, descargue el archivo zip (vinculado arriba) y descomprímalo. Luego, en su terminal, navegue por la carpeta del repositorio.

Puede comprobar que está en el lugar correcto ejecutando `ls` y ver una lista de archivos, incluido `install-cube.sh`. 
## Paso 2: inicie los contenedores

Es posible que deba actualizar su archivo docker-compose.yml local iniciando los contenedores: 
* Abra el archivo `docker-compose.yml` en su editor de texto
* Bajo el servicio `jupyter`, cambie los puertos (`ports`) de `"80:8888"` a `"8888:8888"`
* Agregue `JUPYTER_ALLOW_INSECURE_WRITES=true` bajo `jupyter`:`environment`

Ejecute el comando:

`docker-compose up -d`

Esto iniciará la base de datos PostgreSQL y los contenedores Jupyters. Debería ver la siguiente salida:</br>
`Starting 2021-better-working-world-data-challenge_postgres_1 ... done`</br>
`Starting 2021-better-working-world-data-challenge_jupyter_1  ... done`

Posteriormente puede utilizar `docker-compose stop` para detener los contenedores (para evitar que use su CPU y memoria).
Para reiniciarlo, ejecute `docker-compose start`. Asegúrese de estar ejecutando los comandos desde la carpeta del repositorio.

## Paso 3: Poblar el Data Cube

Este paso cargará los datos de imágenes indexadas en la base de datos.</br>

Si tiene la herramienta `make` instalada (muy probable si está en MacOS/Linux) simplemente puede ejecutar el comando siguiente:</br>
`make prepare`</br>
Si no tiene "make", y está en MacOS, Linux, o está usando Cygwin o WSL en Windows puede ejecutar:
`./install-cube.sh - true` </br>
Si está usando el CMD de Windows, puede ser que necesite ejecutar cada uno de los comandos siguientes: </br>
Inicializar la BBDD datacube </br>
`docker-compose exec jupyter datacube -v system init`

Agregar metadata adecuada </br>
`docker-compose exec jupyter datacube metadata add /scripts/data/metadata.eo_plus.yaml `</br>
`docker-compose exec jupyter datacube metadata add /scripts/data/eo3_landsat_ard.odc-type.yaml` 

Agregar algunas definiciones de productos</br>
`docker-compose exec jupyter datacube product add /scripts/data/ga_s2a_ard_nbar_granule.odc-product.yaml`</br>
`docker-compose exec jupyter datacube product add /scripts/data/ga_s2b_ard_nbar_granule.odc-product.yaml `</br>`
docker-compose exec jupyter datacube product add /scripts/data/ga_ls7e_ard_3.odc-product.yaml`</br>`
docker-compose exec jupyter datacube product add /scripts/data/ga_ls8c_ard_3.odc-product.yaml`</br>`
docker-compose exec jupyter datacube product add /scripts/data/linescan.odc-product.yaml` </br>
Ahora indexar algunos datasets</br>
`docker-compose exec jupyter bash -c "dc-index-from-tar --protocol https --ignore-lineage -p ga_ls7e_ard_3 -p ga_ls8c_ard_3 /scripts/data/ls78.tar.gz"`</br>`
docker-compose exec jupyter bash -c "dc-index-from-tar --protocol https --ignore-lineage -p ga_s2a_ard_nbar_granule -p ga_s2b_ard_nbar_granule /scripts/data/s2ab.tar.gz"`</br>`
docker-compose exec jupyter bash -c "dc-index-from-tar --protocol https --ignore-lineage -p linescan /scripts/data/linescan.tar.gz"`

## Paso 4: Abrir Jupyter
Si todo fue exitoso, ahora usted puede acceder su Jupyter local.
Luego diríjase a [http://localhost:8888/](http://localhost:8888/) e ingrese el password "secretpassword" para ingresar.
Le será requerido un password que está seteado como `secretpassword`. No se preocupe, sólo los usuarios en su computadora pueden acceder aquí.
Si realizó el cambio en el paso 2 para usar el puerto 8888, use [http://localhost:8888/](http://localhost:8888/)

## Paso 5: Dirijase al archivo [Modelo.md](https://github.com/UTN-FRM-TUP/Grupo-I-TT/blob/master/Modelo.md) para generar el modelo de machine learning y su subsiguiente salida.
