# 🗂️ Navix — Explorador Terminal con Vista de Imágenes

**Navix** es un explorador de archivos minimalista para terminal, diseñado para entornos Wayland con Kitty.  
Compatible con Hyprland, modular por diseño, y enfocado en control explícito y reversibilidad quirúrgica.

🧠 Ideal para usuarios que valoran:
- Interfaces sin distracciones
- Navegación rápida por teclado
- Integración con scripts personalizados
- Visualización de imágenes en terminal (Kitty)

🔧 Compatible con Linux (Arch, Fedora, Ubuntu) y entornos Wayland.

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

## 📦 Requisitos

- Python 3.10+ recomendado  
- Compatible con versiones ≥ 3.8 (no testeado formalmente)

> ⚠️ Aunque Navix fue desarrollado y probado con Python 3.10+, muchos módulos utilizados existen desde Python 3.8. Si decides probarlo en versiones anteriores, es posible que funcione correctamente. Se agradecen reportes de compatibilidad.

---

## Uso Basico

- ↑ ↓ para navegar
- Enter para abrir imágenes, reproducir videos o mostrar texto
- x para marcar archivos
- c para copiar
- v para vizualizar fotos en la terminal kitty
- d para borrar
- Usa --dry-run para simular acciones sin modificar archivos.

---

🛠️ Compatibilidad

Navix ha sido probado en:

Arch Linux + Hyprland + Kitty Fedora y Ubuntu con entorno Wayland Terminales compatibles con kitty +kitten icat

---

🤝 Contribuciones

Se aceptan mejoras, refactorizaciones modulares y reportes de compatibilidad. Puedes abrir un issue o enviar un pull request con tus cambios.

---

📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

## 🧪 Instalación recomendada (global con `pipx`)

```bash
git clone https://github.com/Brextal/navix.git
cd navix
pipx install .
navix
