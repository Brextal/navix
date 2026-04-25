#!/bin/bash

# Verificar si el script tiene permisos de ejecución (solo útil si se ejecuta con bash install.sh)
if [ ! -x "$0" ]; then
    echo "❌ Este script no tiene permisos de ejecución. Usa:"
    echo "    chmod +x install.sh && ./install.sh"
    exit 1
fi

echo "🛠️ Instalador de Navix — Explorador Terminal con Vista de Imágenes"

# Detectar si estamos dentro del directorio navix
if [ ! -f "setup.py" ]; then
    echo "📁 No se detectó setup.py. ¿Estás fuera del directorio navix?"
    if [ -d "navix" ]; then
        echo "📦 Entrando al directorio navix..."
        cd navix
    else
        echo "❌ No se encontró el directorio navix. Clona el repositorio primero:"
        echo "    git clone https://github.com/Brextal/navix.git"
        exit 1
    fi
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
source .venv/bin/activate

# Instalar Navix localmente
echo "🚀 Instalando Navix..."
pip install .

# Crear symlink global en ~/.local/bin
mkdir -p "$HOME/.local/bin"
ln -sf "$PWD/.venv/bin/navix" "$HOME/.local/bin/navix"

# Verificar si ~/.local/bin está en el PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo ""
    echo "⚙️ Agregando ~/.local/bin al PATH..."

    # Agregar a .bashrc
    if [ -f "$HOME/.bashrc" ]; then
        if ! grep -q '~/.local/bin' "$HOME/.bashrc"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        fi
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    fi

    # Agregar a .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        if ! grep -q '~/.local/bin' "$HOME/.zshrc"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        fi
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    fi

    echo "✅ PATH actualizado. Ejecuta 'source ~/.bashrc' o abre una nueva terminal."
fi

# Verificar si el comando quedó disponible
if command -v navix &> /dev/null; then
    echo ""
    echo "✅ Instalación completada. Ejecuta Navix con:"
    echo "    navix"
    echo ""
    echo "🖼️ Usa terminal Kitty para ver imágenes correctamente."
    navix
else
    echo "⚠️ El comando 'navix' no está en el PATH del entorno. Ejecuta manualmente con:"
    echo "source .venv/bin/activate && navix"
fi
