### FILE: common/ocr.py
"""
Funciones de lectura de PDF con soporte OCR si el PDF está escaneado.
Usa pdfplumber para PDFs nativos y pytesseract + pdf2image para escaneados.
"""
import io
import re
from pdf2image import convert_from_path
import pdfplumber
import pytesseract
from PIL import Image


def is_scanned_pdf(path_pdf):
    """Detecta si el PDF contiene texto seleccionable o no."""
    try:
        with pdfplumber.open(path_pdf) as pdf:
            for page in pdf.pages[:3]:
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    return False
    except Exception:
        pass
    return True


def ocr_pdf(path_pdf, dpi=300):
    """Convierte cada página a imagen y aplica OCR."""
    pages = convert_from_path(path_pdf, dpi=dpi)
    texts = []
    for p in pages:
        text = pytesseract.image_to_string(p, lang='spa')
        texts.append(text)
    return '\n'.join(texts)


def extract_text_with_pdfplumber(path_pdf):
    lines = []
    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.append(text)
    return '\n'.join(lines)


def load_text_from_pdf(path_pdf):
    if is_scanned_pdf(path_pdf):
        print('Documento escaneado detectado — aplicando OCR (pytesseract)')
        return ocr_pdf(path_pdf)
    else:
        print('PDF nativo detectado — extrayendo texto con pdfplumber')
        return extract_text_with_pdfplumber(path_pdf)

