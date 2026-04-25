from pathlib import Path
from datetime import datetime
import os

LOG_DIR = Path.home() / ".navix_logs"
LOG_FILE = LOG_DIR / "eventos.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.touch(exist_ok=True)
os.chmod(str(LOG_DIR), 0o700)
os.chmod(str(LOG_FILE), 0o600)

def log_event(tipo: str, mensaje: str, ruta: str = None) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruta_str = f" | {ruta}" if ruta else ""
    linea = f"[{timestamp}] [{tipo}] {mensaje}{ruta_str}\n"
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(linea)
    except Exception:
        pass  # Fallo silencioso

def log_error(e: Exception, contexto: str = "") -> None:
    mensaje = f"{contexto}: {e}"
    log_event("ERROR", mensaje)
