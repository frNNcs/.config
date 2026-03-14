# Configuración de Ollama con opencode

Guía detallada para integrar Ollama con opencode server.

## Instalación de Ollama

### Linux

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verificar instalación
ollama --version
```

### Servicio systemd

```bash
# /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Service
After=network-online.target
Wants=network-online.target

[Service]
Type=exec
User=ubuntu
ExecStart=/usr/local/bin/ollama serve
Environment="OLLAMA_HOST=0.0.0.0:11434"
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## Modelos Recomendados

### Modelos para desarrollo general

| Modelo | Tamaño | VRAM | Uso |
|--------|--------|------|-----|
| llama3.2 | 3.8GB | ~4GB | General, rápido |
| llama3.2:7b | 3.8GB | ~4GB | Balanceado |
| qwen2.5:7b | 4.4GB | ~5GB | Excelente reasoning |
| mistral | 4.1GB | ~4GB | Rápido, eficiente |

### Modelos para código

| Modelo | Tamaño | VRAM | Uso |
|--------|--------|------|-----|
| codellama | 3.8GB | ~4GB | Código general |
| deepseek-coder | 3.8GB | ~4GB | Código especializado |
| codeqwen | 4.2GB | ~5GB | Código + chat |

### Modelos pequeños (para pruebas)

| Modelo | Tamaño | VRAM |
|--------|--------|------|
| llama3.2:1b | 1.3GB | ~2GB |
| phi3 | 2.3GB | ~3GB |
| mistral:7b | 4.1GB | ~4GB |

---

## Gestión de Modelos

### Listar modelos

```bash
ollama list
```

### Descargar modelo

```bash
ollama pull llama3.2
ollama pull codellama
ollama pull deepseek-coder
```

### Eliminar modelo

```bash
ollama rm llama3.2
```

### Ver modelo info

```bash
ollama show llama3.2
```

---

## Configuración de opencode para Ollama

### Método 1: Via TUI

1. Iniciar opencode: `opencode --hostname servidor --port 4096`
2. Presionar `Ctrl+P` para abrir configuración
3. Buscar "providers" o "Ollama"
4. Configurar API base: `http://localhost:11434`

### Método 2: Via API

```bash
# Configurar Ollama como provider
curl -X PATCH http://localhost:4096/config \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{
    "providers": {
      "ollama": {
        "apiBase": "http://localhost:11434",
        "models": ["llama3.2", "codellama", "qwen2.5"]
      }
    }
  }'
```

### Método 3: Via config file

En el servidor, crear `~/.config/opencode/config.json`:

```json
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434",
      "defaultModel": "llama3.2"
    }
  }
}
```

---

## Configuración Avanzada

### Variables de entorno de Ollama

```bash
# Puerto de escucha
OLLAMA_HOST=0.0.0.0:11434

# Modelos a cargar al inicio
OLLAMA_MODELS=/path/to/models

# Número de threads
OLLAMA_THREADS=8

# VRAM disponible (GB)
OLLAMA_VRAM=16

# Timeout de запрос
OLLAMA_TIMEOUT=300
```

### Optimización de rendimiento

```bash
# Para servidor con 16GB VRAM
OLLAMA_VRAM=16 ollama serve

# Para servidor con 32GB VRAM
OLLAMA_VRAM=32 ollama serve
```

---

## Troubleshooting Ollama

### Error: connection refused

```bash
# Verificar que Ollama esté corriendo
systemctl status ollama

# Ver logs
journalctl -u ollama -n 50

# Reiniciar
sudo systemctl restart ollama
```

### Error: model not found

```bash
# Listar modelos disponibles
ollama list

# Descargar modelo
ollama pull nombre-del-modelo
```

### Error: out of memory

```bash
# Reducir uso de VRAM
export OLLAMA_VRAM=8
sudo systemctl restart ollama
```

---

## Script: Instalar y Configurar Ollama

```bash
#!/bin/bash
set -e

echo "Instalando Ollama..."

# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Crear servicio
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=exec
User=$USER
ExecStart=/usr/local/bin/ollama serve
Environment="OLLAMA_HOST=0.0.0.0:11434"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Esperar y descargar modelo
sleep 5
ollama pull llama3.2

echo "Ollama instalado y modelo descargado"
```
