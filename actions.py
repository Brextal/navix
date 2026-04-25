from pathlib import Path
import shutil
import subprocess
import curses
import os
from utils import confirmar
from log import log_event, log_error

def copiar_archivo(stdscr, origen, destino_base, dry_run=False):
    origen_p = Path(origen)
    destino_dir = Path(destino_base)
    alto, _ = stdscr.getmaxyx()

    base = origen_p.stem
    ext = origen_p.suffix

    for i in range(1, 1000):
        destino_p = destino_dir / f"{base}_copia{i}{ext}"
        if destino_p.exists():
            continue
        else:
            break
    else:
        stdscr.addstr(alto - 3, 2, "❌ Demasiadas copias. Abortado.", curses.A_BOLD)
        log_event("ERROR", "Demasiadas copias generadas", str(origen_p))
        return

    if dry_run:
        stdscr.addstr(alto - 3, 2, f"🔎 Simulación: copiaría como {destino_p.name}", curses.A_DIM)
        log_event("SIMULACIÓN", f"Copiaría {origen_p} a {destino_p}", str(origen_p))
        return

    try:
        shutil.copy2(origen_p, destino_p)
        stdscr.addstr(alto - 3, 2, f"✅ Copiado como: {destino_p.name}", curses.A_DIM)
        log_event("COPIA", f"Archivo copiado a {destino_p}", str(origen_p))
    except Exception as e:
        stdscr.addstr(alto - 3, 2, f"❌ Error al copiar: {e}", curses.A_BOLD)
        log_error(e, f"Error al copiar {origen_p}")


def mover_archivo(stdscr, origen, destino, dry_run=False):
    origen_p = Path(origen)
    destino_p = Path(destino).expanduser().resolve()
    alto, _ = stdscr.getmaxyx()

    # ✅ Validación robusta
    if not destino:
        stdscr.addstr(alto - 3, 2, "❌ Ruta vacía. Movimiento cancelado.", curses.A_BOLD)
        log_event("ERROR", "Ruta destino vacía", str(origen_p))
        return

    if not destino_p.exists():
        stdscr.addstr(alto - 3, 2, f"❌ Ruta no existe: {destino_p}", curses.A_BOLD)
        log_event("ERROR", "Ruta destino no existe", str(destino_p))
        return

    if not destino_p.is_dir():
        stdscr.addstr(alto - 3, 2, f"❌ Ruta no es carpeta: {destino_p}", curses.A_BOLD)
        log_event("ERROR", "Ruta destino no es carpeta", str(destino_p))
        return

    if not os.access(destino_p, os.W_OK):
        stdscr.addstr(alto - 3, 2, f"❌ Sin permisos de escritura en: {destino_p}", curses.A_BOLD)
        log_event("ERROR", "Sin permisos de escritura", str(destino_p))
        return

    destino_final = destino_p / origen_p.name

    if destino_final.exists():
        stdscr.addstr(alto - 3, 2, f"❌ Ya existe: {destino_final}", curses.A_BOLD)
        log_event("ERROR", "Destino ya existe", str(destino_final))
        return

    if dry_run:
        stdscr.addstr(alto - 3, 2, f"🔎 Simulación: movería a {destino_final}", curses.A_DIM)
        log_event("SIMULACIÓN", f"Movería {origen_p} a {destino_final}", str(origen_p))
        return

    try:
        shutil.move(str(origen_p), str(destino_final))
        stdscr.addstr(alto - 3, 2, f"✅ Movido a: {destino_final}", curses.A_DIM)
        log_event("MOVER", f"Archivo movido a {destino_final}", str(origen_p))
    except Exception as e:
        stdscr.addstr(alto - 3, 2, f"❌ Error al mover: {e}", curses.A_BOLD)
        log_error(e, f"Error al mover {origen_p}")


def eliminar_archivo(stdscr, ruta, nombre, dry_run=False, confirmado=False):
    ruta_p = Path(ruta)
    es_carpeta = ruta_p.is_dir()

    if confirmado:
        if es_carpeta:
            if not confirmar(stdscr, f"⚠️ '{nombre}' es una CARPETA. ¿Confirmar borrado definitivo?"):
                return
    elif es_carpeta:
        if not confirmar(stdscr, f"¿Eliminar CARPETA '{nombre}'?"):
            return
        if not confirmar(stdscr, f"⚠️ Confirmar borrado de '{nombre}' (NO SE PUEDE DESHACER)?"):
            return
    elif not confirmar(stdscr, f"¿Eliminar '{nombre}'?"):
        return

    if dry_run:
        stdscr.addstr(1, 2, f"🔎 Simulación: eliminaría {nombre}", curses.A_DIM)
        log_event("SIMULACIÓN", f"Eliminaría {nombre}", str(ruta_p))
        return
    try:
        if ruta_p.is_dir():
            shutil.rmtree(ruta_p)
        else:
            ruta_p.unlink()
        stdscr.addstr(1, 2, f"✅ Eliminado: {nombre}", curses.A_DIM)
        log_event("BORRADO", f"Elemento eliminado: {nombre}", str(ruta_p))
    except Exception as e:
        stdscr.addstr(1, 2, f"❌ Error al borrar: {e}", curses.A_BOLD)
        log_error(e, f"Error al borrar {ruta_p}")

def ver_archivo(stdscr, ruta, nombre):
    ruta_p = Path(ruta)
    if not ruta_p.is_file():
        return False

    ext = ruta_p.suffix.lower()

    # Ignorar videos completamente desde 'v'
    if ext in ('.mp4', '.webm', '.mkv', '.avi', '.mov'):
        return False
    
    

    try:
        # Solo salir de curses si el archivo es compatible
        if ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.txt', '.md', '.log'):
            curses.endwin()

        if ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'):
            subprocess.run(["kitty", "+kitten", "icat", str(ruta_p)], check=False)
            subprocess.run(["bash", "-c", "read -n 1 -s -r -p 'Presiona ENTER para cerrar...'; exit 0"], check=False)
            subprocess.run(["kitty", "+kitten", "icat", "--clear"], check=False)

        elif ext in ('.txt', '.md', '.log'):
            with ruta_p.open('r', encoding='utf-8') as f:
                preview = ''.join(f.readlines()[:30])
            subprocess.run([
                "zenity", "--info", "--title=Vista previa: " + nombre,
                "--width=600", "--height=400", "--text", preview
            ], check=True, text=True)

        else:
            return False

        # Restaurar curses y redibujar explorador
        curses.reset_prog_mode()
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        curses.doupdate()

        log_event("VISTA", f"Archivo mostrado: {nombre}", str(ruta_p))
        return True

    except Exception as e:
        log_error(e, f"Error al mostrar archivo {ruta_p}")
        return False
