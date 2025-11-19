#!/bin/bash
# Script para forzar reconfiguración de padding cuando hay problemas

echo "=== Forzando reconfiguración de padding ==="
echo "Fecha: $(date)"

# Matar cualquier proceso display_watcher anterior
pkill -f "display_watcher.sh" 2>/dev/null || true

# Limpiar estado previo
rm -f "$HOME/.config/yabai/.display_state" 2>/dev/null || true

echo "Detectando configuración actual..."

# Ejecutar setup_padding.sh
"$HOME/.config/yabai/setup_padding.sh"

echo "Reiniciando display watcher..."

# Reiniciar display watcher
"$HOME/.config/yabai/display_watcher.sh" &

echo "Reconfiguración forzada completada"
echo "Verificando estado final:"

# Mostrar configuración actual
echo "Top padding actual: $(yabai -m config top_padding)"
echo "Displays activos:"
yabai -m query --displays | jq -r '.[] | "Display \(.index): \(.frame.w)x\(.frame.h)"'
