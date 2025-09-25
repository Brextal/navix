from pathlib import Path
import curses
import subprocess
from utils import icono_archivo, obtener_info, abrir_archivo, confirmar, pedir_ruta
from actions import copiar_archivo, mover_archivo, eliminar_archivo as borrar_archivo, ver_archivo


class Explorador:
    def __init__(self, stdscr, ruta_base, dry_run=False):
        self.stdscr = stdscr
        self.archivos_marcados = set()
        base = Path(ruta_base).expanduser()
        self.ruta_actual = base.resolve() if base.exists() else Path.home().resolve()
        self.archivo_copiado = None
        self.imagen_mostrada = None
        self.seleccion = 0
        self.offset = 0
        self.dry_run = dry_run

    def run(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.curs_set(0)

        while True:
            if self.imagen_mostrada is None:
                subprocess.run(["kitty", "+kitten", "icat", "--clear"], check=False)
                self.render()

            tecla = self.stdscr.getch()

            if self.imagen_mostrada is not None:
                if tecla in (curses.KEY_UP, curses.KEY_DOWN):
                    self.imagen_mostrada = None
                    subprocess.run(["kitty", "+kitten", "icat", "--clear"], check=False)
                    self.render()
                continue

            if not self.handle_input(tecla):
                break

    def verificar_archivo_copiado(self):
        if self.archivo_copiado and not self.archivo_copiado.exists():
            self.archivo_copiado = None

    def render(self):
        self.verificar_archivo_copiado()
        self.stdscr.clear()
        alto, ancho = self.stdscr.getmaxyx()
        max_ancho = ancho - 4
        max_visible = alto - 6
        self.stdscr.addstr(0, 0, f"📁 {self.ruta_actual}"[:max_ancho], curses.A_BOLD)

        try:
            contenido = [p.name for p in sorted(self.ruta_actual.iterdir()) if not p.name.startswith('.')]
        except PermissionError:
            contenido = []

        total = len(contenido)
        if total == 0:
            self.stdscr.addstr(2, 2, "(carpeta vacía)", curses.A_DIM)

        if self.seleccion < self.offset:
            self.offset = self.seleccion
        elif self.seleccion >= self.offset + max_visible:
            self.offset = self.seleccion - max_visible + 1

        for idx in range(self.offset, min(self.offset + max_visible, total)):
            nombre = contenido[idx]
            ruta_p = self.ruta_actual / nombre

            try:
                info = obtener_info(ruta_p)
            except Exception:
                info = "error"

            prefijo = icono_archivo(ruta_p) + " "
            nombre_visible = (prefijo + nombre)[:max_ancho - len(info) - 3]
            linea = f"{nombre_visible} — {info}"

            estilo = curses.A_NORMAL
            if ruta_p in self.archivos_marcados:
                estilo = curses.color_pair(2)
                if idx == self.seleccion:
                    estilo |= curses.A_REVERSE
            elif self.archivo_copiado and self.archivo_copiado.exists() and ruta_p.samefile(self.archivo_copiado):
                estilo = curses.color_pair(1)
                if idx == self.seleccion:
                    estilo |= curses.A_REVERSE
            elif idx == self.seleccion:
                estilo = curses.A_REVERSE

            try:
                self.stdscr.addstr(idx - self.offset + 2, 2, linea, estilo)
            except curses.error:
                pass

        mensaje = "↑↓: navegar | Enter: abrir/entrar | ⌫: volver | c: copiar | p: pegar | m: mover | d: borrar | v: ver | x: marcar | ESC: salir"
        self.stdscr.addstr(alto - 2, 0, mensaje[:ancho - 1], curses.A_DIM)
        self.stdscr.refresh()

    def handle_input(self, tecla):
        try:
            contenido = [p.name for p in sorted(self.ruta_actual.iterdir()) if not p.name.startswith('.')]
        except PermissionError:
            contenido = []

        total = len(contenido)

        if tecla == curses.KEY_UP and self.seleccion > 0:
            self.seleccion -= 1
        elif tecla == curses.KEY_DOWN and self.seleccion < total - 1:
            self.seleccion += 1
        elif tecla in (curses.KEY_ENTER, 10, 13) and total > 0:
            ruta_p = self.ruta_actual / contenido[self.seleccion]
            if ruta_p.is_dir():
                self.ruta_actual = ruta_p
                self.seleccion = 0
                self.offset = 0
            else:
                abrir_archivo(ruta_p)
        elif tecla == ord('c') and total > 0:
            ruta_p = self.ruta_actual / contenido[self.seleccion]
            if ruta_p.is_file():
                self.archivo_copiado = ruta_p
        elif tecla == ord('p'):
            if self.archivos_marcados:
                for ruta in self.archivos_marcados:
                    copiar_archivo(self.stdscr, str(ruta), str(self.ruta_actual), self.dry_run)
                self.archivos_marcados.clear()
            elif self.archivo_copiado:
                copiar_archivo(self.stdscr, str(self.archivo_copiado), str(self.ruta_actual), self.dry_run)
                self.archivo_copiado = None
        elif tecla == ord('x') and total > 0:
            ruta_p = self.ruta_actual / contenido[self.seleccion]
            if ruta_p in self.archivos_marcados:
                self.archivos_marcados.remove(ruta_p)
            else:
                self.archivos_marcados.add(ruta_p)
        
        elif tecla == ord('m') and total > 0:
            curses.endwin()
            print(f"\nRuta actual: {self.ruta_actual}\n")
            destino = pedir_ruta().strip()
            curses.doupdate()
            self.stdscr = curses.initscr()

            if not destino:
                self.render()
                return True

            destino_path = Path(destino).expanduser().resolve()

            if not destino_path.exists() or not destino_path.is_dir():
                self.stdscr.clear()
                self.stdscr.addstr(1, 2, f"❌ Ruta inválida o no es carpeta: {destino}", curses.A_BOLD)
                self.stdscr.refresh()
                self.stdscr.getch()
                return True

            if self.archivos_marcados:
                for ruta in list(self.archivos_marcados):
                    mover_archivo(self.stdscr, str(ruta), str(destino_path), self.dry_run)
                self.archivos_marcados.clear()
            else:
                ruta_p = self.ruta_actual / contenido[self.seleccion]
                mover_archivo(self.stdscr, str(ruta_p), str(destino_path), self.dry_run)

            self.seleccion = 0
            self.offset = 0

        elif tecla == ord('d') and total > 0:
            self.stdscr.clear()
            self.stdscr.refresh()
            if self.archivos_marcados:
                nombres = [ruta.name for ruta in self.archivos_marcados]
                lista = "\n".join(f"• {n}" for n in nombres)
                confirmar_texto = f"¿Eliminar los siguientes {len(nombres)} archivos?\n\n{lista}"
                if confirmar(self.stdscr, confirmar_texto):
                    for ruta in list(self.archivos_marcados):
                        borrar_archivo(self.stdscr, str(ruta), ruta.name, self.dry_run, confirmado=True)
                    self.archivos_marcados.clear()
            else:
                ruta_p = self.ruta_actual / contenido[self.seleccion]
                if confirmar(self.stdscr, f"¿Eliminar {ruta_p.name}?"):
                    borrar_archivo(self.stdscr, str(ruta_p), ruta_p.name, self.dry_run)
            self.seleccion = 0
            self.offset = 0

        elif tecla == ord('v') and total > 0:
            ruta_p = self.ruta_actual / contenido[self.seleccion]
            nombre = contenido[self.seleccion]
            if self.imagen_mostrada != nombre:
                if ver_archivo(self.stdscr, str(ruta_p), nombre):
                    self.imagen_mostrada = None
                    self.render()

        elif tecla in (curses.KEY_BACKSPACE, 127, 8):
            padre = self.ruta_actual.parent
            if padre != self.ruta_actual:
                self.ruta_actual = padre
                self.seleccion = 0
                self.offset = 0

        elif tecla == 27:
            return False

        return True
