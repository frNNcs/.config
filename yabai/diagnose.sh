#!/bin/bash
# Script de diagnóstico para problemas de padding

echo "=== DIAGNÓSTICO YABAI PADDING ==="
echo "Fecha: $(date)"
echo

echo "1. ESTADO DE DISPLAYS:"
yabai -m query --displays | jq -r '.[] | "Display \(.index): \(.frame.w)x\(.frame.h) [\(.label // "Sin nombre")]"'
echo

echo "2. CONFIGURACIÓN ACTUAL:"
echo "   Top padding: $(yabai -m config top_padding)"
echo "   Bottom padding: $(yabai -m config bottom_padding)"
echo "   Left padding: $(yabai -m config left_padding)"
echo "   Right padding: $(yabai -m config right_padding)"
echo "   Window gap: $(yabai -m config window_gap)"
echo

echo "3. CONFIGURACIÓN POR ESPACIO:"
yabai -m query --spaces | jq -r '.[] | "Espacio \(.index): top_padding=\(.["top-padding"] // "default")"' 2>/dev/null || echo "   No se pudo obtener información de espacios"
echo

echo "4. PROCESOS ACTIVOS:"
pgrep -f "display_watcher.sh" > /dev/null && echo "   ✅ display_watcher.sh ejecutándose" || echo "   ❌ display_watcher.sh NO ejecutándose"
pgrep -f "lid_monitor.sh" > /dev/null && echo "   ✅ lid_monitor.sh ejecutándose" || echo "   ❌ lid_monitor.sh NO ejecutándose"
echo

echo "5. LOGS RECIENTES:"
echo "   Display watcher log (últimas 5 líneas):"
if [ -f "$HOME/.config/yabai/display_watcher.log" ]; then
    tail -5 "$HOME/.config/yabai/display_watcher.log" | sed 's/^/     /'
else
    echo "     No existe log de display_watcher"
fi
echo

echo "   Lid monitor log (últimas 5 líneas):"
if [ -f "$HOME/.config/yabai/lid_events.log" ]; then
    tail -5 "$HOME/.config/yabai/lid_events.log" | sed 's/^/     /'
else
    echo "     No existe log de lid_monitor"
fi
echo

echo "6. ESTADO ESPERADO vs ACTUAL:"
displays=$(yabai -m query --displays)
display_count=$(echo "$displays" | jq length)

if [ "$display_count" -eq 1 ]; then
    width=$(echo "$displays" | jq -r '.[0].frame.w')
    height=$(echo "$displays" | jq -r '.[0].frame.h')
    
    if (( $(echo "$width <= 1800 && $height <= 1200" | bc -l) )); then
        expected_padding=12
        echo "   Configuración detectada: Solo laptop"
    else
        expected_padding=46
        echo "   Configuración detectada: Solo monitor externo"
    fi
else
    external_display=$(echo "$displays" | jq -r '.[] | select(.frame.w == 1920 and .frame.h == 1080)')
    if [ -n "$external_display" ]; then
        expected_padding=46
        echo "   Configuración detectada: Multi-display con monitor externo"
    else
        expected_padding=12
        echo "   Configuración detectada: Multi-display sin monitor externo"
    fi
fi

current_padding=$(yabai -m config top_padding)
echo "   Padding esperado: ${expected_padding}px"
echo "   Padding actual: ${current_padding}px"

if [ "$expected_padding" -eq "$current_padding" ]; then
    echo "   ✅ Configuración correcta"
else
    echo "   ❌ Configuración incorrecta - ejecutar force_reconfig.sh"
fi

echo
echo "=== FIN DIAGNÓSTICO ==="
