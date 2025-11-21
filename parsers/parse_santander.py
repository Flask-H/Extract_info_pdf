### FILE: parsers/parse_santander.py
"""
Parser para contratos Santander basados en palabras clave y bloques.
"""
import re


def parse(text):
    t = text
    # Buscar bloque PRESTATARIO
    m = re.search(r'PRESTATARIO(.*?)(?:FIADOR|FINANCIADOR|$)', t, flags=re.DOTALL | re.IGNORECASE)
    block = m.group(1) if m else t

    # Nombre: intentar buscar líneas con 'Nombre:' o dos apellidos + nombre
    nombre = None
    m_n = re.search(r'Nombre\s*[:\-]?\s*([A-Za-zÁÉÍÓÚÑáéíóúñ\. ]{3,100})', block, flags=re.IGNORECASE)
    if m_n:
        nombre = m_n.group(1).strip()
    else:
        # fallback heurístico: buscar primera línea con 2-3 palabras
        for line in block.split('\n'):
            l = line.strip()
            if len(l.split()) >= 2 and len(l) < 60:
                nombre = l
                break

    email = None
    m_e = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", block)
    if m_e:
        email = m_e.group(0)

    nif = None
    m_nif = re.search(r"\b\d{7,8}[A-Z]\b", block)
    if m_nif:
        nif = m_nif.group(0)

    telefono = None
    m_tel = re.search(r"\b(6|7|8|9)\d{8}\b", block)
    if m_tel:
        telefono = m_tel.group(0)

    direccion = None
    m_dir = re.search(r'(Domicil(?:io|io)[:\s]*)(.+)', block, flags=re.IGNORECASE)
    if m_dir:
        direccion = m_dir.group(2).split('\n')[0].strip()

    # CP/poblacion/provincia heurística
    cp = poblacion = provincia = None
    m_loc = re.search(r'(\d{5})\s*-?\s*([A-Za-zÁÉÍÓÚÑáéíóúñ\-\. ]+?)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', block)
    if m_loc:
        cp, poblacion, provincia = m_loc.group(1), m_loc.group(2).strip(), m_loc.group(3).strip()

    return {
        'tipo': 'santander',
        'nombre': nombre,
        'nif': nif,
        'email': email,
        'telefono': telefono,
        'direccion': direccion,
        'cp': cp,
        'poblacion': poblacion,
        'provincia': provincia,
    }

