#!/bin/bash

# Configuración
HOST="${OPENCODE_HOST:-localhost}"
PORT="${OPENCODE_PORT:-4096}"
USER="${OPENCODE_USER:-opencode}"
PASSWORD="${OPENCODE_PASSWORD:-}"

URL="http://${HOST}:${PORT}"
AUTH="-u ${USER}:${PASSWORD}"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  opencode Server Status${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Verificar health
echo -e "${YELLOW}Health Check:${NC}"
HEALTH=$(curl -s ${URL}/global/health 2>/dev/null)
if [ $? -eq 0 ] && echo "$HEALTH" | grep -q "healthy"; then
    VERSION=$(echo "$HEALTH" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    echo -e "  ${GREEN}✓${NC} Servidor ejecutándose"
    echo -e "  ${GREEN}✓${NC} Versión: $VERSION"
else
    echo -e "  ${RED}✗${NC} Servidor no disponible"
    exit 1
fi
echo ""

# Verificar config
echo -e "${YELLOW}Configuración:${NC}"
if [ -n "$PASSWORD" ]; then
    CONFIG=$(curl -s ${URL}/config ${AUTH} 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} Autenticación exitosa"
    else
        echo -e "  ${RED}✗${NC} Error de autenticación"
    fi
else
    echo -e "  ${YELLOW}!${NC} Sin autenticación configurada"
fi
echo ""

# Listar proveedores
echo -e "${YELLOW}Proveedores:${NC}"
PROVIDERS=$(curl -s ${URL}/provider ${AUTH} 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "$PROVIDERS" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | while read p; do
        echo -e "  - $p"
    done
else
    echo -e "  ${RED}✗${NC} No se pudo obtener proveedores"
fi
echo ""

# Listar sesiones
echo -e "${YELLOW}Sesiones:${NC}"
SESSIONS=$(curl -s ${URL}/session ${AUTH} 2>/dev/null)
if [ $? -eq 0 ]; then
    COUNT=$(echo "$SESSIONS" | grep -o '"id"' | wc -l)
    echo -e "  ${GREEN}✓${NC} $COUNT sesión(es) activa(s)"
else
    echo -e "  ${RED}✗${NC} No se pudieron listar sesiones"
fi
echo ""

# Listar modelos (si es accesible)
echo -e "${YELLOW}Modelos Ollama:${NC}"
curl -s http://${HOST}:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | while read m; do
    echo -e "  - $m"
done
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo -e "  ${YELLOW}!${NC} Ollama no disponible en puerto 11434"
fi
echo ""

echo -e "${BLUE}========================================${NC}"
