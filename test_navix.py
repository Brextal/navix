import unittest
import tempfile
import os
from pathlib import Path
import sys
import shutil

sys.path.insert(0, str(Path(__file__).parent))

from utils import icono_archivo, obtener_info, EXTENSIONESPeligrosas
from log import LOG_DIR, LOG_FILE


class TestIconoArchivo(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_icono_carpeta(self):
        carpeta = self.temp_path / "carpeta_test"
        carpeta.mkdir()
        self.assertEqual(icono_archivo(carpeta), "📁")

    def test_icono_py(self):
        archivo = self.temp_path / "test.py"
        archivo.touch()
        self.assertEqual(icono_archivo(archivo), "🐍")

    def test_icono_imagen(self):
        for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            archivo = self.temp_path / f"imagen{ext}"
            archivo.touch()
            self.assertEqual(icono_archivo(archivo), "🖼️")

    def test_icono_ejecutable(self):
        archivo = self.temp_path / "exec"
        archivo.touch()
        os.chmod(str(archivo), 0o755)
        self.assertEqual(icono_archivo(archivo), "⚙️")


class TestObtenerInfo(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_archivo_simple(self):
        archivo = self.temp_path / "test.txt"
        archivo.write_text("contenido")
        info = obtener_info(archivo)
        self.assertIn("KB", info)
        fecha = info.split(" — ")[-1]
        self.assertIn("-", fecha)

    def test_carpeta_vacia(self):
        carpeta = self.temp_path / "vacia"
        carpeta.mkdir()
        info = obtener_info(carpeta)
        self.assertIn("0 KB", info)

    def test_symlink_roto(self):
        objetivo = self.temp_path / "no_existe"
        link = self.temp_path / "link_roto"
        link.symlink_to(objetivo)
        info = obtener_info(link)
        self.assertEqual(info, "🔗 roto")


class TestExtensionesPeligrosas(unittest.TestCase):
    def test_lista_no_vacia(self):
        self.assertGreater(len(EXTENSIONESPeligrosas), 0)

    def test_contiene_scripts(self):
        self.assertIn(".sh", EXTENSIONESPeligrosas)
        self.assertIn(".py", EXTENSIONESPeligrosas)
        self.assertIn(".js", EXTENSIONESPeligrosas)

    def test_es_set(self):
        self.assertIsInstance(EXTENSIONESPeligrosas, (set, frozenset))


class TestLog(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_log_dir_existe(self):
        self.assertTrue(LOG_DIR.exists())
        self.assertTrue(LOG_DIR.is_dir())

    def test_log_file_existe(self):
        self.assertTrue(LOG_FILE.exists())
        self.assertTrue(LOG_FILE.is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)