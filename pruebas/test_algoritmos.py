import importlib.util
import unittest
from pathlib import Path
ruta=Path(__file__).resolve().parent.parent/"python"/"benchmark.py"
spec=importlib.util.spec_from_file_location("metodos",ruta)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Pruebas(unittest.TestCase):
    def test_metodos(self):
        casos=[[],[1.0],[3.5,-2.1,0,3.5],[500,-500,0.01,-0.01],mod.datos(500,77)]
        for f in (mod.bubble,mod.merge,mod.tree,mod.heap,mod.counting):
            for caso in casos:
                a=caso.copy()
                resultado=f(a)
                self.assertEqual(sorted(caso),resultado if resultado is not None else a)

if __name__=="__main__":
    unittest.main()
