### FILE: parsers/parse_generic.py
"""
Parser genérico usando regex robustos para campos comunes.
"""
import re


def find_nif(text):
    m = re.search(r"\b\d{7,8}[A-Z]\b", text)
    return m.group(0) if m else None


def find_email(text):
    m = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    return m.group(0) if m else None


def find_phone(text):
    m = re.search(r"\b(6|7|8|9)\d{8}\b", text)
    return m.group(0) if m else None


def find_cp_pob_prov(text):
    m = re.search(r'(\d{5})\s+([A-Za-zÁÉÍÓÚÑáéíóúñ\-\. ]+)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', text)
    if m:
        return m.group(1), m.group(2).strip(), m.group(3).strip()
    return None, None, None


def parse(text):
    return {
        'tipo': 'generic',
        'nombre': None,
        'nif': find_nif(text),
        'email': find_email(text),
        'telefono': find_phone(text),
        'direccion': None,
        'cp': find_cp_pob_prov(text)[0],
        'poblacion': find_cp_pob_prov(text)[1],
        'provincia': find_cp_pob_prov(text)[2],
    }

