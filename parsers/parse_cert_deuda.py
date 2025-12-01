# parsers/parse_cert_deuda.py
import re

def parse(text):
    """
    Parser del Certificado de Deuda.
    Extrae únicamente la CUANTÍA, buscando patrones robustos.
    """

    data = {
        "tipo": "certificado_deuda",
        "cuantia": ""
    }

    # ================================
    # 1. Patrón robusto "XXX.XXX,XX€"
    # ================================
    patron_cuantia = r"\b\d{1,3}(?:\.\d{3})*,\d{2}\s*€?"

    encontrados = re.findall(patron_cuantia, text)

    if not encontrados:
        return data  # se devuelve sin cuantía

    # Convertir a número para elegir el mayor
    valores = []
    for numero in encontrados:
        num_clean = numero.replace("€", "").strip()
        try:
            valor_float = float(num_clean.replace(".", "").replace(",", "."))
            valores.append((valor_float, numero))
        except:
            pass

    if not valores:
        return data

    # Tomamos el mayor porque suele ser "importe total adeudado"
    mayor = sorted(valores, key=lambda x: x[0], reverse=True)[0][1]

    data["cuantia"] = mayor.strip()

    return data