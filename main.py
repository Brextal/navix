#!/usr/bin/env python3
import locale
import curses
import sys
from pathlib import Path
from core import Explorador

def main():
    dry_run = "--dry-run" in sys.argv
    locale.setlocale(locale.LC_ALL, '')
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    try:
        explorador = Explorador(stdscr, Path.home(), dry_run)
        explorador.run()
    except Exception as e:
        curses.endwin()
        print("❌ Error inesperado:", e)
        import traceback
        traceback.print_exc()
        input("Presiona ENTER para salir...")
    finally:
        try:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
        except Exception:
            pass


if __name__ == "__main__":
    main()
