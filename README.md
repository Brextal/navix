# 🗂️ Navix — Explorador Terminal con Vista de Imágenes

Explorador de archivos minimalista para terminal, con soporte para visualización directa de imágenes usando `kitty +kitten icat`. Diseñado para usuarios que valoran el control explícito, la reversibilidad y la estética sobria.

---

## 🚀 Características

- Navegación por carpetas con interfaz `curses`
- Vista directa de imágenes (`.png`, `.jpg`, `.webp`, etc.) en terminal Kitty
- Soporte para copiar, mover, borrar y marcar archivos
- Confirmación única para acciones múltiples
- Modo `--dry-run` para simulaciones sin modificar archivos
- Compatible con `mpv` para reproducir videos (solo con `Enter`)
- Compatible con `zenity` para vista previa de texto plano
- Registro persistente de eventos en `~/.navix_logs`
- Autocompletado de rutas con validación interactiva (`prompt_toolkit`)
- Tamaño real de carpetas calculado dinámicamente

---

## 📦 Requisitos

- Python 3.10+ recomendado  
- Puede funcionar en versiones anteriores (≥ 3.8), pero no ha sido probado formalmente

> ⚠️ Nota: Aunque Navix fue desarrollado y probado con Python 3.10+, muchos módulos utilizados existen desde Python 3.8. Si decides probarlo en versiones anteriores, es posible que funcione correctamente. Se agradecen reportes de compatibilidad.

---

## 🧪 Instalación recomendada (global con `pipx`)

```bash
git clone https://github.com/Brextal/navix.git
cd navix
pipx install .
navix
