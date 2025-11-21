### FILE: parsers/parse_peugeot_from_uploaded.py
"""
Esta versión importa y reutiliza el extractor_manteniment.py que subiste.
Si quieres usar directamente el archivo que subiste, copia extractor_manteniment.py
al directorio parsers/ y renómbralo o impórtalo.

A modo de ejemplo, este archivo muestra cómo envolver la lógica existente.
"""
from pathlib import Path

# Si has subido extractor_manteniment.py en el mismo directorio de trabajo
# y quieres reutilizarlo directamente, puedes importar su contenido.
# Aquí mostramos cómo hacerlo dinámicamente: buscar el archivo en la ruta dada.

import importlib.util
import sys

UPLOADED = 'extractor_manteniment.py'  # ruta relativa al directorio de ejecución


def parse_using_uploaded(text=None, path=None):
    # Si el usuario prefiere que el parser use el archivo subido, se puede ejecutar así
    if path is None:
        path = UPLOADED
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'No se encontró {path} para reutilizar')

    spec = importlib.util.spec_from_file_location('extractor_manteniment', str(p))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # El archivo original expone funciones que imprimen datos; ajusta si es necesario.
    # Aquí, simplemente ejecutamos su flujo principal si define main-like behavior.
    if hasattr(module, 'extraer_texto_preciso'):
        # si sólo queremos pasar texto, devuelva parse(text)
        if text:
            return module.extraer_datos_universal(text)
        else:
            # si sólo hay ruta, intenta ejecutar y capturar
            return module.extraer_datos_universal(module.extraer_texto_preciso(path))
    else:
        raise RuntimeError('El módulo subido no tiene la API esperada')

