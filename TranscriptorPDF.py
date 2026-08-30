import pymupdf
import re

documento = pymupdf.open(
    r"C:\Users\sergio\Desktop\programacioncurso\2doAño\programacion phyton\Unidad Didáctica 1 - Aprendizaje de Máquina y Programación Python.pdf"
)

encontrado_esquema = False
numeracion_pendiente = None

with open("extraccion.txt", "w", encoding="utf-8") as archivo:

    for pagina in documento:

        texto = pagina.get_text()

        

        if re.search(r"Esquema de Contenidos", texto, re.IGNORECASE):
               
         lineas = texto.splitlines()

         for linea in lineas:

            linea = linea.strip()

            if not linea:
                    continue

            resultado = re.match(
                    r"^(\d+(?:\.\d+)*)\.?(?:\s+(.*))?$",
                    linea
                )

            if resultado:

                    numero = resultado.group(1)
                    titulo = resultado.group(2)

                    if titulo:
                        archivo.write(f"{numero} {titulo}\n")

                    else:
                        numeracion_pendiente = numero

            elif numeracion_pendiente:

                    archivo.write(f"{numeracion_pendiente} {linea}\n")
                    numeracion_pendiente = None
         break