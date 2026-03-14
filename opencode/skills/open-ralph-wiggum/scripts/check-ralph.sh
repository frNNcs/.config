#!/usr/bin/env bash
# check-ralph.sh - Diagnóstico del entorno Open Ralph Wiggum + Ollama
# Uso: bash check-ralph.sh

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ok() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo ""
echo "=== Open Ralph Wiggum - Diagnóstico de Entorno ==="
echo ""

# Bun
echo "--- Runtime ---"
if command -v bun &> /dev/null; then
  ok "Bun: $(bun --version)"
else
  fail "Bun no instalado. Instalar: curl -fsSL https://bun.sh/install | bash"
fi

# Ralph
echo ""
echo "--- Ralph Wiggum ---"
if command -v ralph &> /dev/null; then
  ok "ralph: $(ralph --version 2>/dev/null || echo 'instalado')"
else
  fail "ralph no instalado. Instalar: bun add -g @th0rgal/ralph-wiggum"
fi

# OpenCode
echo ""
echo "--- Agentes ---"
if command -v opencode &> /dev/null; then
  ok "opencode: $(opencode --version 2>/dev/null || echo 'instalado')"
else
  warn "opencode no encontrado (opcional si usas otro agente)"
fi

if command -v claude &> /dev/null; then
  ok "claude-code: instalado"
else
  warn "claude-code no encontrado (opcional)"
fi

# Ollama
echo ""
echo "--- Ollama ---"
if command -v ollama &> /dev/null; then
  ok "ollama: $(ollama --version 2>/dev/null || echo 'instalado')"
  
  # Verificar si ollama está corriendo
  if curl -s --max-time 2 http://localhost:11434/api/tags &> /dev/null; then
    ok "Ollama API: respondiendo en localhost:11434"
    
    # Listar modelos
    MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "")
    if [ -n "$MODELS" ]; then
      ok "Modelos disponibles:"
      while IFS= read -r model; do
        echo "   - $model"
      done <<< "$MODELS"
    else
      warn "No hay modelos descargados. Ejecutar: ollama pull qwen2.5-coder:7b"
    fi
  else
    warn "Ollama instalado pero no corriendo. Ejecutar: ollama serve"
  fi
else
  fail "Ollama no instalado. Ver: https://ollama.ai"
fi

# Config opencode
echo ""
echo "--- Configuración opencode ---"
OPENCODE_CONFIG="$HOME/.config/opencode/opencode.json"
if [ -f "$OPENCODE_CONFIG" ]; then
  ok "Config encontrada: $OPENCODE_CONFIG"
  if grep -q "ollama" "$OPENCODE_CONFIG" 2>/dev/null; then
    ok "Ollama configurado en opencode.json"
  else
    warn "Ollama no configurado en opencode.json"
    echo "   Añadir: {\"providers\": {\"ollama\": {\"apiBase\": \"http://localhost:11434\"}}}"
  fi
else
  warn "No existe $OPENCODE_CONFIG"
fi

# Estado ralph en directorio actual
echo ""
echo "--- Estado del Proyecto Actual ---"
if [ -d ".ralph" ]; then
  ok "Directorio .ralph encontrado"
  [ -f ".ralph/ralph-loop.state.json" ] && ok "Loop state: .ralph/ralph-loop.state.json" || true
  [ -f ".ralph/ralph-tasks.md" ] && ok "Tasks: .ralph/ralph-tasks.md" || true
  [ -f ".ralph/ralph-history.json" ] && ok "History: .ralph/ralph-history.json" || true
else
  warn "No hay directorio .ralph en el directorio actual (normal si no se ha ejecutado ralph aquí)"
fi

echo ""
echo "=== Diagnóstico completo ==="
echo ""
echo "Para ejecutar ralph con Ollama:"
echo "  ralph \"tu tarea aquí. Responde <promise>COMPLETE</promise> cuando termines\" \\"
echo "    --agent opencode --model ollama/qwen2.5-coder:7b --max-iterations 10"
echo ""
