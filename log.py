from pathlib import Path
from datetime import datetime

LOG_DIR = Path.home() / ".navix_logs"
LOG_FILE = LOG_DIR / "eventos.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_event(tipo: str, mensaje: str, ruta: str = None) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruta_str = f" | {ruta}" if ruta else ""
    linea = f"[{timestamp}] [{tipo}] {mensaje}{ruta_str}\n"
    try:
        LOG_FILE.write_text(linea, encoding="utf-8", append=True)
    except TypeError:
        # Para versiones de pathlib sin append
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(linea)
    except Exception:
        pass  # Fallo silencioso

def log_error(e: Exception, contexto: str = "") -> None:
    mensaje = f"{contexto}: {e}"
    log_event("ERROR", mensaje)
