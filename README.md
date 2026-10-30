# Práctica 2: algoritmos de ordenamiento

Materia: Análisis y Diseño de Algoritmos.

Integrantes: Rosas Ríos Luis Gabriel, García Mata Leonardo y Cruz Rodríguez Aldo Giovanni Baruch.

Se implementaron Bubble Sort, Merge Sort, Tree Sort, Heap Sort y Counting Sort en C++ y Python. El objetivo es medir sus tiempos y el consumo de memoria con arreglos de números reales de distintos tamaños.

## Contenido

- `cpp/benchmark.cpp`: cinco algoritmos en C++.
- `python/benchmark.py`: cinco algoritmos en Python.
- `herramientas/ejecutar.py`: compila C++, ejecuta las pruebas por separado y guarda los resultados.
- `herramientas/graficas.py`: crea gráficas SVG a partir de los resultados.
- `herramientas/generar_reporte.py`: actualiza las tablas del reporte.
- `pruebas/`: comprobaciones de que los cinco algoritmos producen el mismo resultado que un ordenamiento de referencia.
- `resultados/resultados.csv`: mediciones y pruebas omitidas.
- `documentacion/reporte.md`: reporte de la práctica.

## Requisitos

Python 3.10 o posterior y un compilador C++ con soporte C++17 (`g++`). Para las gráficas no hace falta instalar librerías adicionales.

## Ejecutar

Desde la carpeta principal del proyecto:

```bash
python herramientas/ejecutar.py
python herramientas/graficas.py
python herramientas/generar_reporte.py
```

El comando normal permite hasta 10 millones en C++ y 1 millón en Python, para reducir el riesgo de saturar un equipo. Para ampliar las pruebas cuando se cuente con memoria suficiente:

```bash
python herramientas/ejecutar.py --cpp-max 100000000 --python-max 10000000 --timeout 180
python herramientas/graficas.py
python herramientas/generar_reporte.py
```

También se puede probar un algoritmo por separado:

```bash
g++ -O2 -std=c++17 cpp/benchmark.cpp -o cpp/benchmark
./cpp/benchmark merge 100000 42
python python/benchmark.py merge 100000 42
```

En Windows, la compilación requiere añadir `-lpsapi` y el ejecutable se llama `cpp/benchmark.exe`. Se puede ejecutar todo con el script de `herramientas/ejecutar.py` si `g++` está en el PATH.

## Pruebas de corrección

```bash
python -m unittest discover -s pruebas -p "test_*.py"
g++ -O2 -std=c++17 pruebas/test_algoritmos.cpp -o test_algoritmos
./test_algoritmos
```

## Consideraciones

Se utilizan valores con dos decimales en el intervalo de -500.00 a 500.00. Counting Sort ordena las claves enteras equivalentes a los centésimos. Con números reales de precisión arbitraria no sería válido aplicar directamente Counting Sort.

Los tiempos incluyen solamente el ordenamiento, no la generación ni la verificación. La memoria es el pico residente del proceso completo. Las filas `omitido` en el CSV son ejecuciones que no se realizaron, no mediciones en cero. Bubble Sort está limitado a 5,000 elementos por su complejidad cuadrática; para mil millones de elementos se necesitarían más de 7.45 GiB únicamente para almacenar los números.

Para mayor detalle, consultar [el reporte](documentacion/reporte.md).