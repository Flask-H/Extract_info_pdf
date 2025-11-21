import pdfplumber
import re

# ======================================================
# 1) EXTRACCIÓN PRECISA DEL TEXTO (sin romper líneas)
# ======================================================
def extraer_texto_preciso(ruta_pdf):
    texto_total = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for page in pdf.pages:
            words = page.extract_words(x_tolerance=1, y_tolerance=1)
            linea = []
            last_y = None

            for w in words:
                y = round(w["top"], 1)
                if last_y is None or abs(y - last_y) < 2:
                    linea.append(w["text"])
                else:
                    texto_total.append(" ".join(linea))
                    linea = [w["text"]]
                last_y = y

            if linea:
                texto_total.append(" ".join(linea))

    return "\n".join(texto_total)


# ======================================================
# 2) EXTRACCIÓN POR ZONAS
#    ZONA CLIENTE = desde "Nº Contrato" hasta "VEHÍCULO"
# ======================================================
def extraer_zona(texto, inicio, fin):
    patron = rf"{inicio}(.*?){fin}"
    m = re.search(patron, texto, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


# ======================================================
# 3) FUNCIONES UNIVERSALES PARA EXTRAER DATOS CON PATRONES ROBUSTOS
# ======================================================

# --- Número de contrato ---
def extraer_numero_contrato(texto):
    patron = r"N[º°]?\s*Contrato[^\n]*\n\s*([0-9]{6,15})"
    m = re.search(patron, texto, flags=re.IGNORECASE)
    return m.group(1) if m else None


# --- Nombre / Razón social ---
def extraer_nombre(texto):
    patron = r"Nombre\s*/\s*Razón social\s*([A-Za-zÁÉÍÓÚÑáéíóúñ. ]+)"
    m = re.search(patron, texto, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None


# --- Dirección ---
def extraer_direccion(texto):
    patron = r"(Calle|Carrer|Avda\.?|Avenida|Avinguda|Passeig|Paseo)[^\n]+"
    m = re.search(patron, texto, flags=re.IGNORECASE)
    return m.group(0).strip() if m else None


# --- CP, Población, Provincia ---
def extraer_localizacion(texto):
    # Buscar la línea real (aunque varíe un poco su formato)
    patron_linea = r"C\.?P\.?\s*/\s*Población\s+Provincia\s+([^\n]+)"
    m = re.search(patron_linea, texto, flags=re.IGNORECASE)
    if not m:
        return None

    linea = m.group(1).strip()

    # Ahora sí: extraer CP, pueblo y provincia de esa línea concreta
    patron_detalle = r"(\d{5})\s+(.+)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)$"
    m2 = re.search(patron_detalle, linea)
    if not m2:
        return None

    return {
        "CP": m2.group(1).strip(),
        "Población": m2.group(2).strip(),
        "Provincia": m2.group(3).strip(),
    }


# --- Email ---
def extraer_email(texto):
    m = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", texto)
    return m.group(0) if m else None


# --- NIF ---
def extraer_nif(texto):
    m = re.search(r"\b\d{8}[A-Z]\b", texto)
    return m.group(0) if m else None


# ======================================================
# 4) FUNCIÓN UNIVERSAL QUE UNE TODA LA EXTRACCIÓN
# ======================================================
def extraer_datos_universal(texto):

    # ---- 1. IDENTIFICAR ZONA CLIENTE ----
    zona_cliente = extraer_zona(texto, "Nº Contrato", "VEHÍCULO")

    datos = {}

    # ---- 2. Extraer datos usando patrones y zona cliente ----
    datos["Numero contrato"] = extraer_numero_contrato(texto_preciso)
    datos["Nombre"] = extraer_nombre(zona_cliente)
    datos["Dirección"] = extraer_direccion(zona_cliente)

    loc = extraer_localizacion(zona_cliente)
    if loc:
        datos.update(loc)

    datos["Email"] = extraer_email(zona_cliente)
    datos["NIF"] = extraer_nif(zona_cliente)

    return datos


# ======================================================
# 5) EJECUCIÓN FINAL
# ======================================================
if __name__ == "__main__":
    ruta = "Contrato-stellantis.pdf"

    texto_preciso = extraer_texto_preciso(ruta)
    

    datos = extraer_datos_universal(texto_preciso)

#with open("datos.txt", "w") as archivo:
    #archivo.write("Hola, escribir archivo")
    
print("\n📌 DATOS EXTRAÍDOS:\n")
for k, v in datos.items():
    print(f"{k}: {v}")