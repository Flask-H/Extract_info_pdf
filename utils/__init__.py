### FILE: utils/__init__.py
# módulo util vacío, reservado

""" Para imprimir datos escaneados
    # Carpeta de salida
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    # Nombre final
    txt_path = out_dir / (path_pdf.stem + "_raw.txt")

    # Guardar
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
"""