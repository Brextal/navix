#!/bin/bash

echo "🛠️ Instalador de Navix — Explorador Terminal con Vista de Imágenes"

# Verificar que pipx esté instalado
if ! command -v pipx &> /dev/null; then
    echo "❌ pipx no está instalado. Instalando pipx con el gestor de paquetes..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S python-pipx --noconfirm
    elif command -v apt &> /dev/null; then
        sudo apt install python3-pipx -y
    else
        echo "⚠️ No se detectó un gestor de paquetes compatible. Instala pipx manualmente."
        exit 1
    fi
    pipx ensurepath
    echo "✅ pipx instalado."
fi

# Instalar navix con pipx
echo "🚀 Instalando navix como comando global..."
pipx install .

if [ $? -eq 0 ]; then
    echo "✅ Instalación completada. Puedes ejecutar el explorador con:"
    echo ""
    echo "    navix"
    echo ""
    echo "🖼️ Recuerda usar terminal Kitty para ver imágenes."
    echo "📂 ¡Disfruta de tu explorador modular!"
    navix
else
    echo "❌ Error durante la instalación. Verifica que estés en el directorio correcto y que setup.py esté presente."
    exit 1
fi
