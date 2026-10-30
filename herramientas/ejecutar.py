import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
ALG=("bubble","merge","tree","heap","counting")
TAM=(100000,1000000,10000000,100000000,1000000000)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cpp-max",type=int,default=10000000)
    p.add_argument("--python-max",type=int,default=1000000)
    p.add_argument("--timeout",type=int,default=180)
    p.add_argument("--salida",default=str(BASE/"resultados"/"resultados.csv"))
    a=p.parse_args()
    exe=BASE/"cpp"/("benchmark.exe" if os.name=="nt" else "benchmark")
    comando=["g++","-O2","-std=c++17",str(BASE/"cpp"/"benchmark.cpp"),"-o",str(exe)]
    if os.name=="nt":
        comando.append("-lpsapi")
    subprocess.run(comando,check=True)
    salida=Path(a.salida)
    salida.parent.mkdir(parents=True,exist_ok=True)
    with salida.open("w",encoding="utf-8",newline="") as archivo:
        escritor=csv.writer(archivo)
        escritor.writerow(["lenguaje","algoritmo","n","segundos","memoria_mib","correcto","estado","detalle"])
        for lenguaje in ("cpp","python"):
            for n in TAM:
                for alg in ALG:
                    limite=a.cpp_max if lenguaje=="cpp" else a.python_max
                    if alg=="bubble":
                        fila=[lenguaje,alg,n,"","","","omitido","Complejidad cuadratica"]
                    elif n>limite:
                        fila=[lenguaje,alg,n,"","","","omitido","Limite configurado"]
                    else:
                        cmd=[str(exe)] if lenguaje=="cpp" else [sys.executable,str(BASE/"python"/"benchmark.py")]
                        try:
                            res=subprocess.run(cmd+[alg,str(n),"42"],capture_output=True,text=True,timeout=a.timeout)
                            if res.returncode:
                                fila=[lenguaje,alg,n,"","","","error",res.stderr.strip()[:100]]
                            else:
                                fila=next(csv.reader([res.stdout.strip()]))+["medido",""]
                        except subprocess.TimeoutExpired:
                            fila=[lenguaje,alg,n,"","","","tiempo_agotado",str(a.timeout)]
                    escritor.writerow(fila)
                    archivo.flush()
                    print(lenguaje,alg,n,fila[6],flush=True)

if __name__=="__main__":
    main()
