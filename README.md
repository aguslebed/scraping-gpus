# GPU Price Scraper & Tracker

Este repositorio contiene un sistema completo para la extracción, seguimiento y visualización de precios de placas de video (GPUs) de las principales tiendas de hardware en Argentina. El objetivo del proyecto es automatizar la recolección de precios, llevar un control de stock y conformar un historial para el análisis comparativo del mercado.

## Estructura del Proyecto

El sistema se compone de cuatro piezas fundamentales, todas integradas mediante Docker para asegurar su portabilidad:

1. Scraping (Python): Scripts automatizados que utilizan Playwright y BeautifulSoup4 para navegar por los distintos ecommerce de componentes, extraer información valiosa (precio, marca, stock) y volcarla a la base de datos.
2. Backend (Django): Una API RESTful ligera que procesa la lógica de negocio y provee a los clientes con los datos consolidados y el flujo del historial de precios.
3. Frontend (React + Vite): La interfaz de usuario encargada de presentar las métricas, historiales y un catálogo unificado al consumidor final de manera visual y organizada.
4. Base de Datos (MongoDB): Almacenamiento no relacional elegido para soportar la constante mutación de registros de placas de video y acumular los historiales diarios sin romper estructuras.

## Cómo inicializar el proyecto

Para facilitar el desarrollo y la ejecución en cualquier equipo, todo el entorno está orquestado con Docker. Solamente necesitás contar con Docker y el plugin de Docker Compose instalados.

### 1. Ejecución de la plataforma web

Para levantar la base de datos, el backend y el frontend de forma simultánea, ejecuta el siguiente comando posicionado en la raíz de este proyecto:

```bash
docker compose up -d
```

Una vez finalizada la construcción inicial, la página web estará operativa ingresando a http://localhost:5173 desde tu navegador habitual. La API de lado del servidor se expondrá en el puerto 8000.

### 2. Extracción de datos (Scraping)

A diferencia de la página web que corre perpetuamente, el Scraper funciona bajo demanda como un proceso por lotes. Para iniciar el minado de precios actualizado desde las páginas web y depositar esa nueva información en tu base de datos local, debes ejecutar:

```bash
docker compose run --rm scraper
```

El script descargará los navegadores virtuales, lanzará las extracciones a cada tienda configurada y al finalizar cerrará y borrará su contenedor temporal de tu equipo, dejando intactos los nuevos precios en el volumen de MongoDB.

## Desarrollo

Los directorios de frontend y backend se montan sobre Docker con volúmenes activos. Esto quiere decir que cualquier archivo que modifiques en el código se reflejará al instante en los sistemas ejecutándose.
Si llegas a incorporar dependencias de sistema o paquetes nuevos a través de `package.json` o los `requirements.txt`, no olvides anexar el comando `--build` para que las imágenes incorporen esas librerías:

```bash
docker compose up -d --build
```
