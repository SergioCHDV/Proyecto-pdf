import pymupdf
import re
import pathlib
import tkinter as tk 

def crear_archivo_extraccion(ruta_pdf): 
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

  nombre_txt = ruta_pdf.with_suffix(".txt")

  with open(nombre_txt, "w", encoding="utf-8") as archivo:
    archivo.write(f"{materia.strip()}\n")
    archivo.write(f"{unidad.strip()}\n\n")

    
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
  return nombre_txt
def mover_archivostxt(carpeta_origen, carpeta_destino):
    carpeta_origen = pathlib.Path(carpeta_origen)
    carpeta_destino = pathlib.Path(carpeta_destino)

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    for archivo_txt in carpeta_origen.rglob("*.txt"):
        ruta_destino = carpeta_destino / archivo_txt.name
        archivo_txt.rename(ruta_destino)
def procesar_pdf():

    nombre = entrada.get().strip()

    if not nombre:
        mensaje.config(text="Escribí el nombre de un archivo PDF.")
        return

    ruta_pdf = pathlib.Path(nombre)

    if not ruta_pdf.exists():
        mensaje.config(text="No se encontró el archivo.")
        return

    if ruta_pdf.suffix.lower() != ".pdf":
        mensaje.config(text="El archivo debe ser un PDF.")
        return

    ruta_txt = crear_archivo_extraccion(ruta_pdf)

    mensaje.config(text=f"TXT creado: {ruta_txt}")



ventana = tk.Tk()

ventana.title("Transcriptor de PDFs")
ventana.geometry("500x200")

etiqueta = tk.Label(ventana,text="Ingrese el nombre o ruta del archivo PDF:")

etiqueta.pack()

entrada = tk.Entry(ventana, width=60)
entrada.pack()

boton = tk.Button(ventana,text="Generar TXT",command=procesar_pdf)

boton.pack()

mensaje = tk.Label(ventana, text="")
mensaje.pack()

ventana.mainloop()