# Guía de Dockerización del Proyecto GPUS Scraper

Este archivo documenta la migración del proyecto para funcionar a través de contenedores de Docker.

## ¿Qué se hizo?

1. **Adecuación de Base de Datos**: Se actualizó el código de `backend/crud_gpu/views.py` y `scraping/db.py` para usar la variable de entorno `MONGO_URI`. Ahora pueden conectarse a un host de la red de Docker (ej: `mongodb://db:27017/`) o seguir usando `http://localhost:27017` por defecto si los corrés sin Docker.
2. **Definición de Dependencias**: Se generaron archivos `requirements.txt` individuales y optimizados tanto para tu backend Django como para tu entorno de Scraping en Python.
3. **Múltiples Dockerfiles**:
   - `backend/Dockerfile`: Configura Python y levanta el servidor de Django.
   - `frontend/Dockerfile`: Configura NodeJS e instala Node Modules.
   - `scraping/Dockerfile`: Instala Playwright, descarga Chromium y las demás utilidades.
4. **Orquestación con docker-compose.yml**: Conecta la red de todos los contenedores para que se comuniquen eficientemente, mapea tus volúmenes locales (para que se recargue el código en caliente) y genera la persistencia de MongoDB.

---

## Cómo arrancar el proyecto

Asegúrate de tener **Docker** y **Docker Compose** instalados en tu computadora.

### 1. Iniciar los servicios principales (Frontend, Backend y BD)

Al ejecutar el siguiente comando, Docker va a descargar las imágenes (la primera vez puede tardar un poco mientras instala Playwright y NPM) y lanzar tanto la API como la WEB:

```bash
docker compose up -d
```
El atributo `-d` los hace correr en segundo plano. Podrás acceder a tu app desde tu navegador en **http://localhost:5173** o consultar tu API en **http://localhost:8000/api/...**.

### 2. Ejecutar el Scraper a demanda

Dado que el Scraper suele ser un trabajo por lotes que arranca, extrae todo y termina, le configuramos un "perfil" especial. Para correr una extracción de datos:

```bash
docker compose run --rm scraper python app.py
```
Esto creará el contenedor temporalmente, correrá las rutinas con Playwright en su entorno virtualizado insertando los datos a MongoDB y luego lo eliminará (solo el contenedor, los datos quedan a salvo).

### 3. Ver los logs de la app

Para ver qué está pasando si algo falla (Backend o Frontend):

```bash
docker compose logs -f api
docker compose logs -f web
```

## Cómo rearmar los contenedores si hay cambios

El proyecto fue configurado de manera que **cualquier cambio en tus archivos de código (.py, .jsx, etc)** se vea reflejado **inmediatamente** porque se mapean los volúmenes, por lo que **no tenés que reiniciar los contenedores cada vez que tocas el código**.

### Sin embargo, SÍ debes reconstruir los contenedores cuando:
1. Agregaste o quitaste paquetes en `package.json`.
2. Agregaste nuevas librerías en los instaladores `requirements.txt`.

En ese caso, sólo tenés que apagar y forzar la reconstrucción ejecutando:

```bash
docker compose down
docker compose up -d --build
```

### Cuando agregas una dependencia de npm en el Frontend:

Dado que el contenedor de Web aísla el directorio `node_modules` para optimizar velocidad y evitar mezclar Linux/Windows, si decidís hacer un `npm install nueva_libreria` desde tu consola normal, deberás rearmar el contenedor de frontend especificando:

```bash
docker compose up -d --build web
```
