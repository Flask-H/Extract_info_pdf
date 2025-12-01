import re
from collections import Counter
    
def parse(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    data = {
        "tipo": "stellantis",
        "nombre": "",
        "apellidos": "",
        "nif": "",
        "email": "",
        "telefono": "",
        "direccion": "",
        "cp": "",
        "poblacion": "",
        "provincia": "",
        "numero_contrato": "",
        "NIF_cliente": "A87323705",
    }

    # 1. Buscar línea con apellidos + nombre + NIF
    patron_persona = re.compile(
        r'^([A-ZÁÉÍÓÚÑ ]+)\s+([A-Za-zÁÉÍÓÚñáéíóú ]+)\s+([0-9XYZ][0-9]{7}[A-Z])$'
    )

    for i, line in enumerate(lines):
        m = patron_persona.match(line)
        if m:
            data["apellidos"] = m.group(1).title().strip()
            data["nombre"] = m.group(2).title().strip()
            data["nif"] = m.group(3).strip()

            # Dirección + teléfonos
            dir_parts = lines[i+1].split()
            # Detectar teléfonos al final
            phones = []
            while dir_parts and re.match(r'^\d{6,}$', dir_parts[-1]):
                phones.append(dir_parts.pop())  # elimino el teléfono del final

            phones = list(reversed(phones))  # si hay 2, quedan ordenados

            # Dirección = todo lo que queda
            data["direccion"] = " ".join(dir_parts)

            # Teléfono = el primero encontrado (si existe)
            data["telefono"] = phones[0] if phones else None


            # CP + poblacion + provincia
            cp_line = lines[i+2].split()
            data["cp"] = cp_line[0]
            data["poblacion"] = " ".join(cp_line[1:-1])
            data["provincia"] = cp_line[-1]

            # Email
            data["email"] = lines[i+3].strip()

            #-----------------------------------------
            # 2. Detección robusta del número de contrato
            #-----------------------------------------

            # Buscar todos los números largos (9-12 dígitos)
            all_numbers = re.findall(r'\b\d{9,12}\b', text)

            if all_numbers:
            # Elegimos el número que más veces aparece
                freq = Counter(all_numbers)
                numero_real = freq.most_common(1)[0][0]
                data["numero_contrato"] = numero_real
             
            break
            

    return data
