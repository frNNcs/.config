#!/bin/bash
set -e

echo "=========================================="
echo "  opencode Server Setup"
echo "=========================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables
SERVER_USER="${SERVER_USER:-ubuntu}"
SERVER_HOST="${SERVER_HOST:-192.168.1.42}"
OPENCODE_PORT="${OPENCODE_PORT:-4096}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"
OPENCODE_PASSWORD="${OPENCODE_PASSWORD:-}"

# Función para mostrar estado
status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Verificar argumentos
if [ -z "$1" ]; then
    echo "Uso: $0 <servidor> [usuario] [password]"
    echo ""
    echo "Ejemplos:"
    echo "  $0 192.168.1.42"
    echo "  $0 192.168.1.42 ubuntu mypassword"
    echo "  SERVER_USER=admin $0 192.168.1.42"
    exit 1
fi

SERVER_HOST="$1"
[ -n "$2" ] && SERVER_USER="$2"
[ -n "$3" ] && OPENCODE_PASSWORD="$3"

echo "Configuración:"
echo "  Servidor: $SERVER_USER@$SERVER_HOST"
echo "  Puerto opencode: $OPENCODE_PORT"
echo "  Puerto Ollama: $OLLAMA_PORT"
echo ""

# Verificar conexión SSH
echo "Verificando conexión SSH..."
if ! ssh -o ConnectTimeout=5 "$SERVER_USER@$SERVER_HOST" "echo 'Conexión OK'" 2>/dev/null; then
    error "No se puede conectar al servidor"
    exit 1
fi
status "Conexión SSH verificada"

# Actualizar sistema
echo ""
echo "Actualizando sistema..."
ssh "$SERVER_USER@$SERVER_HOST" "sudo apt update && sudo apt upgrade -y"

# Instalar Ollama
echo ""
echo "Instalando Ollama..."
ssh "$SERVER_USER@$SERVER_HOST" <<'EOF'
curl -fsSL https://ollama.com/install.sh | sh

# Configurar para escuchar en todas las interfaces
sudo systemctl edit ollama --drop-in=override.conf <<'DROPIN'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
DROPIN

sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl restart ollama

# Esperar y descargar modelo
sleep 5
ollama pull llama3.2
EOF
status "Ollama instalado"

# Instalar opencode
echo ""
echo "Instalando opencode..."
ssh "$SERVER_USER@$SERVER_HOST" <<'EOF'
# Instalar opencode
curl -sSL https://opencode.ai/install.sh | sh

# Crear directorio de config
mkdir -p ~/.config/opencode
EOF
status "opencode instalado"

# Configurar opencode service
echo ""
echo "Configurando opencode como servicio..."
ssh "$SERVER_USER@$SERVER_HOST" <<EOF
sudo tee /etc/systemd/system/opencode.service > /dev/null <<'SERVICE'
[Unit]
Description=OpenCode Server
After=network.target

[Service]
Type=simple
User=$SERVER_USER
WorkingDirectory=/home/$SERVER_USER
Environment="OPENCODE_SERVER_PASSWORD=$OPENCODE_PASSWORD"
Environment="OLLAMA_HOST=http://localhost:$OLLAMA_PORT"
ExecStart=/usr/local/bin/opencode serve --hostname 0.0.0.0 --port $OPENCODE_PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable opencode
sudo systemctl start opencode
EOF
status "opencode configurado como servicio"

# Abrir puertos
echo ""
echo "Configurando firewall..."
ssh "$SERVER_USER@$SERVER_HOST" <<EOF
sudo ufw allow $OPENCODE_PORT/tcp 2>/dev/null || true
sudo ufw allow $OLLAMA_PORT/tcp 2>/dev/null || true
sudo ufw reload 2>/dev/null || true
EOF
status "Puertos abiertos"

# Verificar estado
echo ""
echo "Verificando servicios..."
sleep 3

ssh "$SERVER_USER@$SERVER_HOST" "systemctl status ollama --no-pager | head -5"
echo ""
ssh "$SERVER_USER@$SERVER_HOST" "systemctl status opencode --no-pager | head -5"

echo ""
echo "=========================================="
echo "  Instalación completada!"
echo "=========================================="
echo ""
echo "Servicios:"
echo "  - Ollama: http://$SERVER_HOST:$OLLAMA_PORT"
echo "  - opencode: http://$SERVER_HOST:$OPENCODE_PORT"
echo ""
echo "Para conectar desde cliente:"
echo "  opencode --hostname $SERVER_HOST --port $OPENCODE_PORT"
echo ""
echo "Para ver logs:"
echo "  ssh $SERVER_USER@$SERVER_HOST 'sudo journalctl -u opencode -f'"
