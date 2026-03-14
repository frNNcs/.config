---
name: opencode-server
description: This skill should be used when the user asks to "instalar opencode en servidor", "configurar opencode server", "gestionar servidor opencode", "conectar ollama a opencode", "usar API de opencode", "iniciar detener opencode", "configurar opencode con ollama", or needs to manage opencode server deployment, configuration, Ollama integration, or API usage.
version: 0.1.0
---

# opencode-server Skill

Gestión completa de opencode server con Ollama para servidor remoto.

## Propósito

Este skill proporciona procedimientos completos para instalar, configurar, gestionar y usar opencode server con Ollama en un servidor remoto.

## Casos de Uso

### 1. Instalación de opencode en el Servidor

Para instalar opencode en el servidor remoto:

```bash
# Conectar al servidor
ssh usuario@servidor

# Instalar opencode (Linux/macOS)
curl -sSL https://opencode.ai/install.sh | sh

# O mediante npm
npm install -g opencode

# Verificar instalación
opencode --version
```

### 2. Iniciar el Servidor opencode

```bash
# Iniciar servidor básico
opencode serve

# Con puerto específico
opencode serve --port 4096

# Escuchar en todas las interfaces (para acceso remoto)
opencode serve --hostname 0.0.0.0 --port 4096

# Con descubrimiento mDNS
opencode serve --mdns --mdns-domain opencode.local

# Con CORS para desarrollo web
opencode serve --hostname 0.0.0.0 --port 4096 \
  --cors http://localhost:5173 \
  --cors https://app.example.com
```

### 3. Configurar Autenticación

```bash
# Configurar contraseña
OPENCODE_SERVER_PASSWORD=tu-contraseña opencode serve

# Con usuario personalizado
OPENCODE_SERVER_USERNAME=admin \
OPENCODE_SERVER_PASSWORD=tu-contraseña \
opencode serve --hostname 0.0.0.0 --port 4096
```

Para persistencia, agregar al `.bashrc` o crear un systemd service:

```bash
# /etc/systemd/system/opencode.service
[Unit]
Description=OpenCode Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
Environment="OPENCODE_SERVER_PASSWORD=tu-contraseña"
ExecStart=/usr/local/bin/opencode serve --hostname 0.0.0.0 --port 4096
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Conectar Ollama como Proveedor

#### En el servidor con Ollama:

```bash
# Verificar que Ollama esté ejecutándose
ollama list
ollama serve

# Por defecto Ollama escucha en localhost:11434
```

#### Configurar opencode para usar Ollama:

Una vez conectado al servidor opencode (via TUI o API):

```bash
# Configurar provider mediante API
curl -X PATCH http://localhost:4096/config \
  -H "Content-Type: application/json" \
  -u opencode:tu-contraseña \
  -d '{
    "providers": {
      "ollama": {
        "apiBase": "http://localhost:11434"
      }
    }
  }'
```

O mediante el TUI de opencode:
- Seleccionar modelo Ollama disponible
- Configurar como provider predeterminado

#### Modelos recomendados para Ollama:

| Modelo | Uso | VRAM |
|--------|-----|------|
| llama3.2 | General | 4GB |
| qwen2.5 | General | 5GB |
| codellama | Código | 8GB |
| mistral | Rápido | 4GB |
| deepseek-coder | Código | 8GB |

### 5. Gestión del Servidor

#### Verificar estado:

```bash
# Health check
curl http://localhost:4096/global/health

# Estado del servidor
curl http://localhost:4096/global/health \
  -u opencode:tu-contraseña
```

#### Ver configuración:

```bash
curl http://localhost:4096/config \
  -u opencode:tu-contraseña
```

#### Listar proveedores:

```bash
curl http://localhost:4096/provider \
  -u opencode:tu-contraseña
```

### 6. API REST - Operaciones Comunes

#### Crear una sesión:

```bash
curl -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -u opencode:tu-contraseña \
  -d '{"title": "Nueva sesión"}'
```

#### Enviar un mensaje:

```bash
curl -X POST "http://localhost:4096/session/{session-id}/message" \
  -H "Content-Type: application/json" \
  -u opencode:tu-contraseña \
  -d '{
    "parts": [
      {"type": "text", "text": "Hola, ayuda con un archivo README.md"}
    ]
  }'
```

#### Listar sesiones:

```bash
curl http://localhost:4096/session \
  -u opencode:tu-contraseña
```

#### Eliminar sesión:

```bash
curl -X DELETE "http://localhost:4096/session/{session-id}" \
  -u opencode:tu-contraseña
```

### 7. Conectar Cliente Local al Servidor Remoto

En el cliente local:

```bash
# Conectar a servidor remoto
opencode --hostname 192.168.1.42 --port 4096

# O configurar mediante variables de entorno
export OPENCODE_HOST=http://192.168.1.42:4096
export OPENCODE_PASSWORD=tu-contraseña
opencode
```

Para configuración permanente, crear config:

```bash
# ~/.config/opencode/config.json
{
  "server": {
    "hostname": "192.168.1.42",
    "port": 4096
  },
  "auth": {
    "username": "opencode",
    "password": "tu-contraseña"
  }
}
```

### 8. Scripts de Automatización

Consultar scripts útiles en `scripts/`:

- **`scripts/server-setup.sh`** - Script completo de instalación
- **`scripts/check-status.sh`** - Verificar estado del servidor
- **`scripts/ollama-models.sh`** - Listar y gestionar modelos Ollama

### 9. Troubleshooting

#### Problemas comunes:

| Problema | Solución |
|----------|----------|
| Connection refused | Verificar firewall: `sudo ufw allow 4096/tcp` |
| Auth failed | Verificar credenciales en variables de entorno |
| Ollama no conectado | Verificar que Ollama esté corriendo: `ollama list` |
| Puerto en uso | Cambiar puerto: `--port 4097` |

#### Ver logs:

```bash
# Si está corriendo como servicio
sudo journalctl -u opencode -f

# Si está corriendo en terminal
# Los logs aparecen en la terminal
```

## Configuración de Red

### Firewall (Ubuntu/Debian)

```bash
# Abrir puerto para opencode
sudo ufw allow 4096/tcp

# Abrir puerto para Ollama (si se accede remotamente)
sudo ufw allow 11434/tcp

# Verificar
sudo ufw status
```

### SSH Tunnel (alternativo)

Si no quieres exponer puertos directamente:

```bash
# Crear tunnel SSH
ssh -L 4096:localhost:4096 -L 11434:localhost:11434 usuario@servidor

# Luego conectar localmente
opencode --port 4096
```

## Referencias Adicionales

- **`references/server-api.md`** - Documentación completa de la API REST
- **`references/ollama-setup.md`** - Guía detallada de configuración Ollama
- **`references/security.md`** - Mejores prácticas de seguridad
