# Navix — Explorador Terminal con Vista de Imágenes

**Navix** es un explorador de archivos minimalista para terminal, diseñado para entornos Wayland con Kitty.
Compatible con Hyprland, modular por diseño, y enfocado en control explícito.

Ideal para usuarios que valoran:
- Interfaces sin distracciones
- Navegación rápida por teclado
- Integración con scripts personalizados
- Visualización de imágenes en terminal (Kitty)

Compatible con Linux (Arch, Fedora, Ubuntu) y entornos Wayland.

---

## 🚀 Características

- Navegación por carpetas con interfaz `curses`
- Vista directa de imágenes (`.png`, `.jpg`, `.webp`, etc.) en terminal Kitty
- Soporte para copiar, mover, borrar y marcar archivos
- Confirmación única para acciones múltiples
- Modo `--dry-run` para simulaciones sin modificar archivos
- Reproducción de videos con `mpv` (solo con `Enter`)
- Vista previa de texto plano con `zenity`
- Registro persistente de eventos en `~/.navix_logs`
- Autocompletado de rutas con validación interactiva (`prompt_toolkit`)
- Cálculo dinámico del tamaño real de carpetas

---

## 🛡️ Seguridad

- Archivos peligrosos bloqueados (scripts, ejecutables, etc.)
- Validación de extensiones antes de abrir archivos
- Permisos restrictivos en archivos de log
- Verificación de symlinks rotos

---

## 🐛 Correcciones y Mejoras

- Lógica de copias mejorada
- Manejo de symlinks rotos
- Confirmación doble para borrar carpetas
- Compatibilidad con Python 3.8+

---

## Requisitos

- Python 3.8+
- Terminal Kitty con `kitten icat`
- prompt_toolkit

---

## Uso Basico

- ↑ ↓ para navegar
- Enter para abrir imágenes, reproducir videos o mostrar texto
- x para marcar archivos
- c para copiar
- p para pegar
- m para mover
- v para visualizar fotos en la terminal kitty
- d para borrar
- Usa --dry-run para simular acciones sin modificar archivos.

---

## Compatibilidad

Navix ha sido probado en:

Arch Linux + Hyprland + Kitty, Fedora y Ubuntu con entorno Wayland Terminales compatibles con kitty +kitten icat

---

## Tests

Ejecuta los tests con:

```bash
python3 test_navix.py
```

---

## Contribuciones

Se aceptan mejoras, refactorizaciones modulares y reportes de compatibilidad. Puedes abrir un issue o enviar un pull request con tus cambios.

---

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.


---

## Importante

Clonar el repositorio **no instala Navix automáticamente**.
Debes ejecutar el instalador manualmente:

## primero ejecuta:
```bash
git clone https://github.com/Brextal/navix.git
```
---

## luego ejecuta:
```bash
cd navix
pip install -e .
```
---

## Cómo iniciar Navix desde la terminal
Una vez instalado, puedes lanzar Navix desde la terminal escribiendo:

```bash
navix
```