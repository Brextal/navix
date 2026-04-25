from pathlib import Path
import platform
import subprocess
import curses
from datetime import datetime
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.validation import Validator, ValidationError

EXTENSIONESPeligrosas = {'.sh', '.bash', '.zsh', '.py', '.js', '.rb', '.perl', '.php', '.pl', '.exe', '.bin', '.run', '.jar', '.msi', '.com', '.bat', '.cmd', '.ps1', '.scr'}

def icono_archivo(ruta):
    ruta_p = Path(ruta)
    ext = ruta_p.suffix.lower()
    if ruta_p.is_dir():
        return "📁"
    if ext == ".py":
        return "🐍"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff"}:
        return "📷"
    if ext in {".md", ".txt", ".log"}:
        return "📄"
    if ext == ".pdf":
        return "📄"
    if ext in {".zip", ".tar", ".gz", ".7z"}:
        return "📦"
    if ext in {".html", ".htm", ".css", ".js"}:
        return "🌐"
    if ext in {".bin", ".iso", ".img"}:
        return "💾"
    if ext in {".mp4", ".mkv", ".webm"}:
        return "🎞️"
    if ext in {".mp3", ".wav", ".flac"}:
        return "🎵"
    if ruta_p.is_file() and os.access(ruta_p, os.X_OK) and ext == "":
        return "⚙️"
    return "📄"

def abrir_archivo(ruta):
    ruta_p = Path(ruta)
    ext = ruta_p.suffix.lower()

    if ext in EXTENSIONESPeligrosas:
        return False

    sistema = platform.system()
    try:
        if sistema == "Linux":
            subprocess.Popen(["xdg-open", str(ruta_p)])
        elif sistema == "Darwin":
            subprocess.Popen(["open", str(ruta_p)])
        elif sistema == "Windows":
            ruta_p.open()
    except Exception:
        pass

def obtener_info(ruta):
    ruta_p = Path(ruta)
    try:
        if ruta_p.is_symlink() and not ruta_p.exists():
            return "🔗 roto"

        if ruta_p.is_file():
            tamaño = ruta_p.stat().st_size
        elif ruta_p.is_dir():
            archivos = list(ruta_p.glob("*"))[:100]
            if len(archivos) > 500:
                return "📦 grande — carpeta"
            tamaño = sum(f.stat().st_size for f in archivos if f.is_file())
        else:
            tamaño = 0

        fecha = datetime.fromtimestamp(ruta_p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        return f"{tamaño // 1024} KB — {fecha}"
    except Exception:
        return "error"



def confirmar(stdscr, mensaje):
    alto, ancho = stdscr.getmaxyx()
    stdscr.move(1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(1, 2, mensaje + " (y/n/ESC): ", curses.A_BOLD)
    stdscr.refresh()
    tecla = stdscr.getch()
    stdscr.move(1, 0)
    stdscr.clrtoeol()
    if tecla == 27:
        stdscr.addstr(1, 2, "❌ Acción cancelada por ESC", curses.A_DIM)
        stdscr.refresh()
        return False
    return tecla in (ord('y'), ord('Y'))

def pedir_ruta():
    class CarpetaValidator(Validator):
        def validate(self, document):
            texto = document.text.strip()
            ruta = Path(texto).expanduser().resolve()
            if not ruta.exists():
                raise ValidationError(message="❌ La ruta no existe", cursor_position=len(texto))
            if not ruta.is_dir():
                raise ValidationError(message="❌ La ruta no es una carpeta", cursor_position=len(texto))

    return prompt(
        "Ruta destino (⇥ para autocompletar): ",
        completer=PathCompleter(only_directories=True, expanduser=True),
        validator=CarpetaValidator(),
        validate_while_typing=True
    ).strip()

