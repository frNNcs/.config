#!/bin/bash
# Display watcher - Detecta cambios en configuración de displays que yabai no captura

LOGFILE="$HOME/.config/yabai/display_watcher.log"
STATE_FILE="$HOME/.config/yabai/.display_state"

# Función para obtener estado actual de displays
get_display_state() {
    yabai -m query --displays | jq -r '.[] | "\(.index):\(.frame.w)x\(.frame.h)"' | sort
}

# Función para log con timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOGFILE"
}

# Inicializar
log_message "Display watcher iniciado"

# Estado inicial
previous_state=$(get_display_state)
echo "$previous_state" > "$STATE_FILE"

# Monitoreo continuo
while true; do
    sleep 2  # Verificar cada 2 segundos
    
    current_state=$(get_display_state)
    
    # Comparar con estado anterior
    if [ "$current_state" != "$previous_state" ]; then
        log_message "Cambio detectado en displays:"
        log_message "Anterior: $previous_state"
        log_message "Actual: $current_state"
        
        # Ejecutar reconfiguración
        log_message "Ejecutando reconfiguración de padding..."
        "$HOME/.config/yabai/setup_padding.sh" >> "$LOGFILE" 2>&1
        
        # Actualizar estado
        previous_state="$current_state"
        echo "$current_state" > "$STATE_FILE"
        
        log_message "Reconfiguración completada"
    fi
done
