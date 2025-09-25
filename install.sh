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
