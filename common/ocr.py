##FILE: common/ocr.py
import pdfplumber
import numpy as np
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

# Inicializar OCR UNA VEZ
_paddle_ocr = PaddleOCR(
    use_angle_cls=True,
    lang="es",
    det_limit_side_len=8000,
    det_limit_type="max"
)

# -------------------------------------------------
# OCR con PaddleOCR (MODO RIGUROSO)
# -------------------------------------------------
def ocr_pdf_paddle(path_pdf, dpi=600, min_confidence=0.5):
    """
    OCR robusto para contratos escaneados.
    """
    print("Iniciando OCR PaddleOCR...")  # DEBUG
    images = convert_from_path(path_pdf, dpi=dpi)
    texts = []

    for page_num, img in enumerate(images, start=1):
        # PIL -> numpy RGB
        img_np = np.array(img.convert("RGB"))

        result = _paddle_ocr.ocr(
            img_np
        )

        if not result or result[0] is None:
            continue

        for line in result[0]:
            data = line[1]

            # Caso tuple/list
            if isinstance(data, (tuple, list)):
                text = data[0]
                confidence = data[1] if len(data) > 1 else 1.0

            # Caso dict (nuevas versiones)
            elif isinstance(data, dict):
                text = data.get("text", "")
                confidence = data.get("confidence", 1.0)

            else:
                continue

            if confidence >= min_confidence and text.strip():
                texts.append(text)

    # Normalización final
    full_text = "\n".join(texts)
    full_text = normalize_ocr_text(full_text)

    return full_text


# -------------------------------------------------
# Normalización OCR
# -------------------------------------------------
def normalize_ocr_text(text: str) -> str:
    if not text:
        return ""

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) > 1:
            lines.append(line)

    return "\n".join(lines)


# -------------------------------------------------
# PDF nativo
# -------------------------------------------------
def extract_text_with_pdfplumber(path_pdf):
    lines = []
    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.append(text)
    return "\n".join(lines)


# -------------------------------------------------
# Lectura ligera (clasificación)
# -------------------------------------------------
def load_text_from_pdf(path_pdf):
    try:
        return extract_text_with_pdfplumber(path_pdf)
    except Exception:
        return ""

