import csv
from pathlib import Path

base=Path(__file__).resolve().parent.parent
with (base/"resultados"/"resultados.csv").open(encoding="utf-8") as f:
    filas=list(csv.DictReader(f))
dest=base/"documentacion"/"reporte.md"
texto=["# Practica 2: algoritmos de ordenamiento","","Integrantes: Rosas Ríos Luis Gabriel, García Mata Leonardo y Cruz Rodríguez Aldo Giovanni Baruch.","","## Resultados","","Se utilizaron numeros con dos decimales entre -500 y 500. El tiempo no incluye generacion de datos ni verificacion. La memoria es el pico residente del proceso completo.",""]
for lenguaje in ("cpp","python"):
    texto += ["## "+lenguaje.upper(),"","| Algoritmo | Elementos | Tiempo (s) | Memoria (MiB) | Estado |","|---|---:|---:|---:|---|"]
    for r in filas:
        if r["lenguaje"]==lenguaje:
            texto.append(f'| {r["algoritmo"]} | {int(r["n"]):,} | {r["segundos"] or "—"} | {r["memoria_mib"] or "—"} | {r["estado"]} |')
    texto.append("")
texto += ["## Graficas","","![Tiempo](../graficas/tiempos.svg)","","![Memoria](../graficas/memoria.svg)","","## Notas","","Counting Sort usa claves enteras que representan centesimos. Bubble Sort tiene costo O(n²), por lo que se omite en los tamaños principales. Las ejecuciones no realizadas se marcan como omitidas y no representan tiempos de cero.",""]
dest.write_text("\n".join(texto),encoding="utf-8")
