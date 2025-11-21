### FILE: common/cleaner.py
"""
Limpieza y normalización básica del texto.
"""
import re


def normalize_whitespace(text):
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def simple_cleanup(text):
    text = normalize_whitespace(text)
    # eliminar caracteres Unicode extraños comunes de OCR
    text = re.sub(r'[\u200b\u200c\ufeff]', '', text)
    return text

