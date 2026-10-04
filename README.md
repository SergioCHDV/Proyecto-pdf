# Transcriptor de PDFs

Programa desarrollado en Python para extraer información estructurada de archivos PDF y generar un archivo TXT a partir de su contenido.

El programa está pensado para documentos educativos que mantienen una estructura similar, especialmente aquellos que contienen información de la materia, unidad didáctica y un esquema de contenidos con numeración jerárquica.

## Funcionalidades

- Abre y procesa archivos PDF.
- Extrae texto de sus páginas.
- Detecta el nombre de la materia y la unidad mediante expresiones regulares.
- Detecta el apartado **Esquema de Contenidos**.
- Identifica títulos y subtítulos mediante su numeración.
- Genera automáticamente un archivo `.txt` con la información extraída.
- Permite ingresar el nombre o la ruta del PDF desde una interfaz gráfica.
- Informa al usuario si el archivo no existe o si no corresponde a un PDF.

## Tecnologías utilizadas

- **Python**
- **PyMuPDF**: extracción de texto de archivos PDF.
- **re**: búsqueda de patrones mediante expresiones regulares.
- **pathlib**: manejo de rutas y archivos.
- **Tkinter**: creación de la interfaz gráfica.

## Funcionamiento

El programa sigue, de manera general, este proceso:


PDF
 ↓
PyMuPDF
 ↓
Extracción del texto
 ↓
Búsqueda de patrones con expresiones regulares
 ↓
Identificación de materia, unidad y esquema de contenidos
 ↓
Generación del archivo TXT


## Formato del archivo generado

La información encontrada en el esquema de contenidos se guarda manteniendo la numeración de los títulos.

Por ejemplo:


Materia: Aprendizaje de Máquina y Programación Python
Unidad Didáctica 1: Introducción a Python – Primera Parte

2.1 ¿Qué es Python?
2.1.1 Estructura de programa
2.1.2 Preparación del entorno
2.1.3 ¡Hola mundo!
3 Expresiones
3.1 Variables
3.1.1 Tipos de datos


La numeración permite conservar la jerarquía de los contenidos.

## Uso

1. Ejecutar el programa.
2. Ingresar el nombre o la ruta del archivo PDF.
3. Presionar **Generar TXT**.
4. El programa procesa el PDF y genera un archivo `.txt` con el mismo nombre en la ubicación del PDF.


## Restricciones del ejercicio

Este proyecto fue desarrollado teniendo en cuenta las siguientes restricciones:

* No utilizar números de página específicos para encontrar la información.
* No utilizar números de línea específicos.
* Utilizar expresiones regulares basadas en patrones comunes a los documentos.
* El programa debe obtener la información a partir de la estructura del contenido de los PDF y no de posiciones fijadas manualmente.

## Estado del proyecto

Esta versión corresponde a un **prototipo funcional**. El objetivo principal es automatizar la extracción de la estructura de contenidos de los documentos y generar un reporte en formato TXT.


