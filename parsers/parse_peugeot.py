### FILE: parsers/parse_peugeot.py
"""
Parser basado en extractor_manteniment.py que subiste.
He adaptado funciones y las he integrado en la API de parser: parse(text) -> dict
"""
import re


# Reutilizamos el enfoque de extracción por palabras proporcionando funciones robustas

def extract_contract_number(text):
    m = re.search(r'N[º°]?\s*Contrato[^\n]*\n\s*([0-9]{4,20})', text, flags=re.IGNORECASE)
    return m.group(1) if m else None


def extract_field_after_label(text, label):
    # Buscar 'label' y tomar la porción hasta el final de línea
    pat = re.compile(rf'{label}\s*[:\-]?\s*(.+)', re.IGNORECASE)
    m = pat.search(text)
    if m:
        return m.group(1).strip()
    return None


def extract_email(text):
    m = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    return m.group(0) if m else None


def extract_nif(text):
    m = re.search(r"\b\d{7,8}[A-Z]\b", text)
    return m.group(0) if m else None


def parse(text):
    # localizar la sección del cliente si existe
    # buscamos la sección "CLIENTE" o "Nombre / Razón social"
    t = text
    # Nombre
    nombre = None
    # Intenta etiqueta clara
    m = re.search(r'CLIENTE\s*\n(.{1,200})', t, flags=re.IGNORECASE)
    if m:
        # la primera línea tras CLIENTE suele contener nombre
        nombre = m.group(1).strip().split('\n')[0]

    if not nombre:
        nombre = extract_field_after_label(t, r'Nombre\s*/\s*Raz[oó]n social')

    direccion = extract_field_after_label(t, 'Domicilio')

    # CP / Población / Provincia (la hoja original usa: C.P. / Población Provincia)
    m_loc = re.search(r'C\.?P\.?\s*/\s*Poblaci[oó]n\s+Provincia\s+([0-9\sA-Za-zÁÉÍÓÚÑáéíóúñ\-.,]+)', t)
    cp = poblacion = provincia = None
    if m_loc:
        linea = m_loc.group(1).strip()
        m2 = re.search(r"(\d{5})\s+(.+)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)$", linea)
        if m2:
            cp, poblacion, provincia = m2.group(1), m2.group(2).strip(), m2.group(3).strip()

    email = extract_email(t)
    nif = extract_nif(t)
    telefono = None
    m_tel = re.search(r"\b(6|7|8|9)\d{8}\b", t)
    if m_tel:
        telefono = m_tel.group(0)

    return {
        'tipo': 'peugeot',
        'numero_contrato': extract_contract_number(t),
        'nombre': nombre,
        'direccion': direccion,
        'cp': cp,
        'poblacion': poblacion,
        'provincia': provincia,
        'nif': nif,
        'email': email,
        'telefono': telefono,
    }

