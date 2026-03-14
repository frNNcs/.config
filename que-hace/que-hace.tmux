#!/bin/bash
# Que hace? - Script de integración con Tmux
# Este script configura el keybinding para abrir el popup de Que hace?

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar que estamos en tmux
if [ -z "$TMUX" ]; then
    echo "Error: Este script debe ejecutarse desde tmux"
    exit 1
fi

# Configurar keybinding
# Usar ? es coherente con tmux (normalmente muestra ayuda)
tmux bind-key ? run-shell "cd $CURRENT_DIR && python3 -m que_hace popup 2>/dev/null || python3 -m que_hace popup"

echo "✓ Que hace? configurado en tmux"
echo "  Keybinding: Prefix + ?"
echo "  Ubicación: $CURRENT_DIR"
