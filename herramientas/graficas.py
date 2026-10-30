import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent.parent
with (BASE/"resultados"/"resultados.csv").open(encoding="utf-8") as f:
    filas=[r for r in csv.DictReader(f) if r["estado"]=="medido"]
dest=BASE/"graficas"
dest.mkdir(exist_ok=True)
for columna,nombre,eje in (("segundos","tiempos","Tiempo (s)"),("memoria_mib","memoria","Memoria maxima (MiB)")):
    fig,ax=plt.subplots(figsize=(10,6))
    for lenguaje in ("cpp","python"):
        for algoritmo in ("bubble","merge","tree","heap","counting"):
            d=sorted((r for r in filas if r["lenguaje"]==lenguaje and r["algoritmo"]==algoritmo),key=lambda x:int(x["n"]))
            if d:
                ax.plot([int(x["n"]) for x in d],[float(x[columna]) for x in d],marker="o",label=f"{lenguaje} {algoritmo}")
    ax.set(xlabel="Numero de elementos",ylabel=eje,title="Comparacion de algoritmos")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True,alpha=.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(dest/f"{nombre}.svg")
    plt.close(fig)
