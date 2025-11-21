### FILE: classifier/contract_classifier.py
"""
Clasificador simple por palabras clave y scoring.
"""
import re
from common.cleaner import simple_cleanup


KEYWORDS = {
    'santander': ['santander consumer', 'contrato de financiación', 'santander consumer efc'],
    'stellantis': ['asnef', 'stellantis financial', 'stellantis finance', 'modelo f-as-7'],
    'peugeot': ['contrato de mantenimiento', 'psag automóviles', 'mantenimiento premium', 'psag automóviles comercial españa'],
}


def classify_contract(text):
    t = simple_cleanup(text.lower())
    scores = {k: 0 for k in KEYWORDS}
    for k, words in KEYWORDS.items():
        for w in words:
            if w in t:
                scores[k] += 1
    # elegir mayor puntuación
    winner = max(scores, key=lambda k: scores[k])
    if scores[winner] == 0:
        return 'generic'
    return winner

