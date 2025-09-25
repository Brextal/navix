#!/bin/bash

echo "🛠️ Instalador local de Navix — Explorador Terminal con Vista de Imágenes"

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
    echo "✅ Instalación completada. Ejecutando Navix..."
    navix
else
    echo "⚠️ El comando 'navix' no está en el PATH del entorno. Ejecuta manualmente con:"
    echo "source .venv/bin/activate && navix"
fi
