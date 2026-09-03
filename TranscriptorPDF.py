import pymupdf
import re
import pathlib


def crear_archivo_extraccion(ruta_pdf,):
  documento = pymupdf.open(ruta_pdf)

  materia = ""
  unidad = ""

  leyendo_materia = False
  leyendo_unidad = False
  termino_encabezado = False
  numeracion_pendiente = None

  for pagina in documento:
    texto = pagina.get_text()

    for linea in texto.splitlines():
        linea = linea.strip()

        if not linea:
            continue

        
        if not leyendo_materia and not materia:
            coincidencia_materia = re.match(r"^Materia\s*:\s*(.*)$",linea,re.IGNORECASE)

            if coincidencia_materia:
                materia = coincidencia_materia.group(0).strip()
                leyendo_materia = True
                continue

        
        if leyendo_materia:
            coincidencia_unidad = re.match(r"^Unidad(?:\s+Didáctica)?\s+\d+\s*[:\-–]\s*(.*)$",linea,re.IGNORECASE)

            if coincidencia_unidad:
                leyendo_materia = False
                unidad = coincidencia_unidad.group(0).strip()
                leyendo_unidad = True
                continue

            materia += " " + linea
            continue

        
        if leyendo_unidad:
            if re.match(
                r"^(?:Prof\.?|Profesor|Lic\.?|Licenciado)\s*:?",linea,re.IGNORECASE):
                leyendo_unidad = False
                termino_encabezado = True
                break

            unidad += " " + linea

    if termino_encabezado:
        break

  with open("extraccion.txt", "w", encoding="utf-8") as archivo:
    archivo.write(f"{materia.strip()}\n")
    archivo.write(f"{unidad.strip()}\n\n")

    # Buscar el esquema
    for pagina in documento:
        texto = pagina.get_text()

        if re.search(r"Esquema de Contenidos", texto, re.IGNORECASE):

            lineas = texto.splitlines()

            ignorando_unidad = False

            for linea in lineas:
                linea = linea.strip()

                if not linea:
                    continue

                if re.match(r"^\s*Unidad(?:\s+Didáctica)?\s*\d+",linea,re.IGNORECASE):
                    ignorando_unidad = True
                    continue

                if ignorando_unidad and not re.match(r"^\d+(?:\.\d+)*\.?(?:\s+.*)?$",linea):
                    continue    
                ignorando_unidad = False

                
                if re.search(r"^\s*\d*\.?\s*Esquema de Contenidos",linea,re.IGNORECASE):
                    continue

                resultado = re.match(r"^(\d+(?:\.\d+)*)\.?(?:\s+(.*))?$",linea)

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
  documento.close()



carpeta=pathlib.Path(r"C:\Users\sergio\Desktop\Material programacion")

for archivo_pdf in carpeta.rglob("*.pdf"):
    crear_archivo_extraccion(archivo_pdf)