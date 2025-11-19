#!/bin/bash
# Script para manejar eventos de abrir/cerrar pantalla del laptop

# Usar pmset para detectar cuando la pantalla se abre/cierra
# y system_profiler para detectar cambios de hardware

LOGFILE="$HOME/.config/yabai/lid_events.log"

log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOGFILE"
}

# Función para detectar si el laptop está abierto o cerrado
is_laptop_open() {
    # Verificar si el display interno está activo
    local laptop_display=$(yabai -m query --displays | jq -r '.[] | select(.frame.w < 1800 and .frame.h < 1200) | .index')
    [ -n "$laptop_display" ]
}

# Monitorear eventos del sistema
log_event "Iniciando monitor de eventos de pantalla"

# Crear un loop que detecte cambios en el estado de la pantalla
previous_laptop_state=""
if is_laptop_open; then
    previous_laptop_state="open"
else
    previous_laptop_state="closed"
fi

log_event "Estado inicial del laptop: $previous_laptop_state"

while true; do
    sleep 3  # Verificar cada 3 segundos
    
    current_laptop_state=""
    if is_laptop_open; then
        current_laptop_state="open"
    else
        current_laptop_state="closed"
    fi
    
    # Si cambió el estado
    if [ "$current_laptop_state" != "$previous_laptop_state" ]; then
        log_event "Cambio de estado detectado: $previous_laptop_state -> $current_laptop_state"
        
        # Esperar un momento para que el sistema se estabilice
        sleep 2
        
        # Forzar reconfiguración
        log_event "Ejecutando reconfiguración tras cambio de estado"
        "$HOME/.config/yabai/setup_padding.sh" >> "$LOGFILE" 2>&1
        
        previous_laptop_state="$current_laptop_state"
        log_event "Reconfiguración completada"
    fi
done
