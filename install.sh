#!/bin/bash

echo "🛠️ Instalador de Navix — Explorador Terminal con Vista de Imágenes"

# Verificar si pipx está disponible
if command -v pipx &> /dev/null; then
    echo "🚀 Instalando navix como comando global con pipx..."
    pipx install .
else
    echo "⚠️ pipx no está disponible. Instalando globalmente con pip..."
    pip install .
fi

# Verificar si el comando navix quedó disponible
if command -v navix &> /dev/null; then
    echo ""
    echo "✅ Instalación completada. Puedes ejecutar el explorador con:"
    echo ""
    echo "    navix"
    echo ""
    echo "🖼️ Recuerda usar terminal Kitty para ver imágenes."
    echo "📂 ¡Disfruta de tu explorador modular!"
    navix
else
    echo "❌ Error: el comando 'navix' no está disponible en tu PATH."
    echo "Verifica que ~/.local/bin esté en tu PATH o usa pipx para instalación aislada."
    exit 1
fi
