#!/bin/bash
# Script mejorado para configurar padding basado en múltiples displays

# Función para determinar el padding apropiado para un display
get_padding_for_display() {
    local width=$1
    local height=$2
    
    if (( $(echo "$width <= 1800 && $height <= 1200" | bc -l) )); then
        echo 12  # Display laptop
    else
        echo 46  # Display externo
    fi
}

# Detectar todos los displays activos
displays=$(yabai -m query --displays)
display_count=$(echo "$displays" | jq length)

echo "=== Setup Padding - $(date) ==="
echo "Displays detectados: $display_count"

# Si solo hay un display activo
if [ "$display_count" -eq 1 ]; then
    display_info=$(echo "$displays" | jq -r '.[0] | "\(.frame.w) \(.frame.h)"')
    width=$(echo $display_info | cut -d' ' -f1)
    height=$(echo $display_info | cut -d' ' -f2)
    
    padding=$(get_padding_for_display $width $height)
    
    if [ "$padding" -eq 12 ]; then
        echo "Configuración: Solo laptop (${width}x${height}) - padding ${padding}px"
    else
        echo "Configuración: Solo monitor externo (${width}x${height}) - padding ${padding}px"
    fi
    
# Si hay múltiples displays
else
    echo "Configuración multi-display detectada"
    
    # Buscar si hay un monitor externo (1920x1080)
    external_display=$(echo "$displays" | jq -r '.[] | select(.frame.w == 1920 and .frame.h == 1080) | "\(.frame.w) \(.frame.h)"')
    
    if [ -n "$external_display" ]; then
        # Hay monitor externo, usar padding de 46px
        padding=46
        echo "Monitor externo 1920x1080 detectado - usando padding ${padding}px"
    else
        # Solo displays pequeños, usar padding de 12px
        padding=12
        echo "Solo displays compactos detectados - usando padding ${padding}px"
    fi
fi

# Aplicar configuración
yabai -m config top_padding $padding
yabai -m config bottom_padding 12
yabai -m config left_padding 12
yabai -m config right_padding 12

# Aplicar a todos los espacios existentes
yabai -m query --spaces | jq -r '.[].index' | while read space; do
    yabai -m config --space $space top_padding $padding 2>/dev/null || true
done

echo "Configuración aplicada: top_padding=${padding}px"
