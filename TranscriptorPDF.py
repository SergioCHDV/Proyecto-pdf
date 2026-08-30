import pymupdf
import re

documento = pymupdf.open(
    r"C:\Users\sergio\Desktop\programacioncurso\2doAño\programacion phyton\Unidad Didáctica 1 - Aprendizaje de Máquina y Programación Python.pdf"
)

encontrado_esquema = False
numeracion_pendiente = None
materia = None
unidad = None

for pagina in documento:
    texto = pagina.get_text()

    if materia is None:
        m = re.search(r'(?im)^\s*Materia\s*:\s*(.+?)\s*$', texto)
        if m:
            materia = m.group(1).strip()

    if unidad is None:
        u = re.search(r'(?im)^\s*Unidad(?:\s+Didáctica)?\s*\d+\s*[:\-–]\s*(.+?)\s*$', texto)
        if u:
            unidad = u.group(1).strip()

    if materia is not None and unidad is not None:
        break

with open("extraccion.txt", "w", encoding="utf-8") as archivo:
    archivo.write(f"materia : {materia}\n")
    archivo.write(f"unidad : {unidad}\n\n")

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