#!/bin/bash
# Solo reconfigurar padding, evitar restart completo

# Función optimizada para configurar padding dinámicamente
setup_padding() {
    local display_count=$(yabai -m query --displays | jq -r 'length')
    
    # Cache del estado actual para evitar reconfiguración innecesaria
    local current_state_file="$HOME/.config/yabai/.display_state"
    local new_state="displays:$display_count"

    # Verificar si ya está configurado correctamente
    if [ -f "$current_state_file" ] && [ "$(cat "$current_state_file")" = "$new_state" ]; then
        return 0
    fi

    if [ "$display_count" -gt 1 ]; then
        # Múltiples displays: detectar espacios por display y aplicar padding según tipo de display
        echo "Configurando múltiples displays dinámicamente"
        
        # Obtener espacios de cada display y aplicar padding según resolución
        yabai -m query --displays | jq -r '.[] | "\(.id) \(.frame.w) \(.frame.h) \(.spaces | join(" "))"' | while read display_id width height spaces; do
            # Determinar si es laptop (resolución menor) o monitor externo
            if (( $(echo "$width <= 1800 && $height <= 1200" | bc -l) )); then
                # Display laptop: padding 12px
                padding=12
                echo "Display $display_id (laptop ${width}x${height}): aplicando padding $padding a espacios $spaces"
            else
                # Display externo: padding 46px  
                padding=46
                echo "Display $display_id (externo ${width}x${height}): aplicando padding $padding a espacios $spaces"
            fi
            
            # Aplicar padding a todos los espacios de este display
            for space in $spaces; do
                yabai -m config --space $space top_padding $padding 2>/dev/null || true
            done
            
            # Para el display principal, actualizar también la configuración global
            if [ "$display_id" = "1" ] || [ "$display_id" = "$(yabai -m query --displays | jq -r '.[] | select(.["has-focus"] == true) | .id')" ]; then
                yabai -m config top_padding $padding
            fi
        done
    elif [ "$display_count" -eq 1 ]; then
        # Un solo display: detectar tipo y configurar todos los espacios
        local display_info=$(yabai -m query --displays | jq -r '.[0] | "\(.frame.w) \(.frame.h)"')
        local width=$(echo $display_info | cut -d' ' -f1)
        local height=$(echo $display_info | cut -d' ' -f2)
        
        if (( $(echo "$width <= 1800 && $height <= 1200" | bc -l) )); then
            # Solo laptop: padding 12px
            echo "Configurando solo laptop: todos los espacios=12px"
            padding=12
        else
            # Solo monitor externo: padding 46px
            echo "Configurando solo monitor externo: todos los espacios=46px"  
            padding=46
        fi
        
        # Aplicar configuración global y a todos los espacios existentes
        yabai -m config top_padding $padding
        yabai -m config bottom_padding 12
        yabai -m config left_padding 12
        yabai -m config right_padding 12
        
        yabai -m query --spaces | jq -r '.[].index' | while read space; do
            yabai -m config --space $space top_padding $padding 2>/dev/null || true
        done
    fi

    # Guardar el estado actual
    echo "$new_state" > "$current_state_file"
}

# Ejecutar reconfiguración
setup_padding
