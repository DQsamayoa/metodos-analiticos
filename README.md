Proyecto final de métodos analíticos
===================================

Repositorio con el desarrollo para el proyecto final de métodos analíticos

# Objetivos

1. Generar un índice de similitud entre el conjunto de artículos de Arxiv.
2. Utilizar la información de los artículos y sus citas para generar un análsisi de redes y de pagerank.
3. Encontrar artículos similares a:

> Aaron D. Tranter, Harry J. Slatyer, Michael R. Hush, Anthony C. Leung, Jesse L. Everett, Karun V. Paul, Pierre Vernaz-Gris, Ping Koy Lam, Ben C. Buchler, Geoff T. Campbell. **Multiparameter optimisation of a magneto-optical trap using deep learning.** *Nature Communications.* DOI: 10.1038/s41467-018-06847-1

# Proceso

1. Para obtener la información de Arxiv se utilizará el proyecto https://github.com/Mahdisadjadi/arxivscraper
2. Para obtener la información de las citas, el script se basará en el publicado en 
3. El proceso de análisis se realizará en Spark con el uso de Databricks.

# Estructura del proyecto

El repositorio está pensado para mantener la siguiente organización

```
.
+-- LICENSE
+-- README.md
+-- python_scripts
|   +-- get_papers.py
|   +-- get_cites.py
+-- r_scripts
|   +-- uploadS3.R
+-- databricks_scripts
|   +-- 
+-- Reporte
|   +-- Reporte.Rmd
|   +-- tex
|       +-- header.tex
```
donde:

- **get_papers.py** Es el script que extrae los datos; id_arxiv, título, abstract, autor(es), fecha de creación de todos los artículos de Arxiv desde enero de 2000  hasta el el 2019. Estos archivos se guardan por categoría y año en formato *feather*
- **get_cites.py** Realizá una búsqueda por cada id_arxiv en la web de INSPIRE y extrae la información de los artículos que han citado el artículo asociado al id_arxiv.
- **uploadS3.R** Da formato de tablas a los archivos de `artículos` y `citas` para exportarlos a un formato `csv` y cargarlos en un bucket de S3.
- **Reporte.Rmd** Archvio en formato Rmarkdown que genera el reprote (entregable) final del proyecto.
