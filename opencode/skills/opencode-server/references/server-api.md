# API REST Completa - opencode Server

Referencia completa de endpoints disponibles en el servidor opencode.

## Base URL

```
http://<hostname>:<port>
```

## Autenticación

Usar Basic Auth:
- Username: `opencode` (o configurar `OPENCODE_SERVER_USERNAME`)
- Password: `OPENCODE_SERVER_PASSWORD`

## Endpoints

### Global

#### GET /global/health
```bash
curl http://localhost:4096/global/health
```
Respuesta:
```json
{
  "healthy": true,
  "version": "1.0.0"
}
```

#### GET /global/event
```bash
curl http://localhost:4096/global/event
```
Streaming de eventos SSE.

---

### Proyecto

#### GET /project
```bash
curl http://localhost:4096/project
```
Lista todos los proyectos.

#### GET /project/current
```bash
curl http://localhost:4096/project/current
```
Obtener proyecto actual.

---

### Configuración

#### GET /config
```bash
curl http://localhost:4096/config -u opencode:password
```
Obtener configuración completa.

#### PATCH /config
```bash
curl -X PATCH http://localhost:4096/config \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{
    "theme": "dark",
    "language": "es"
  }'
```

#### GET /config/providers
```bash
curl http://localhost:4096/config/providers -u opencode:password
```
Lista proveedores y modelos disponibles.

---

### Proveedores

#### GET /provider
```bash
curl http://localhost:4096/provider -u opencode:password
```
Lista todos los proveedores.

#### GET /provider/auth
```bash
curl http://localhost:4096/provider/auth -u opencode:password
```
Métodos de autenticación disponibles.

---

### Sesiones

#### GET /session
```bash
curl http://localhost:4096/session -u opencode:password
```
Lista todas las sesiones.

#### POST /session
```bash
curl -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{"title": "Mi proyecto"}'
```

#### GET /session/status
```bash
curl http://localhost:4096/session/status -u opencode:password
```
Estado de todas las sesiones.

#### GET /session/:id
```bash
curl http://localhost:4096/session/abc123 -u opencode:password
```

#### DELETE /session/:id
```bash
curl -X DELETE http://localhost:4096/session/abc123 -u opencode:password
```

#### PATCH /session/:id
```bash
curl -X PATCH http://localhost:4096/session/abc123 \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{"title": "Nuevo título"}'
```

---

### Mensajes

#### GET /session/:id/message
```bash
curl "http://localhost:4096/session/abc123/message?limit=10" -u opencode:password
```

#### POST /session/:id/message
```bash
curl -X POST "http://localhost:4096/session/abc123/message" \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{
    "parts": [
      {"type": "text", "text": "Crea un archivo README.md"}
    ]
  }'
```

#### POST /session/:id/prompt_async
```bash
curl -X POST "http://localhost:4096/session/abc123/prompt_async" \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{
    "parts": [{"type": "text", "text": "Hola"}]
  }'
```

---

### Archivos

#### GET /find?pattern=<pat>
```bash
curl "http://localhost:4096/find?pattern=function" -u opencode:password
```

#### GET /find/file?query=<q>
```bash
curl "http://localhost:4096/find/file?query=README" -u opencode:password
```

#### GET /file?path=<path>
```bash
curl "http://localhost:4096/file?path=/home/usuario/proyecto" -u opencode:password
```

#### GET /file/content?path=<path>
```bash
curl "http://localhost:4096/file/content?path=/home/usuario/proyecto/README.md" -u opencode:password
```

---

### TUI Control

#### POST /tui/append-prompt
```bash
curl -X POST http://localhost:4096/tui/append-prompt \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{"text": "texto a agregar"}'
```

#### POST /tui/submit-prompt
```bash
curl -X POST http://localhost:4096/tui/submit-prompt -u opencode:password
```

#### POST /tui/execute-command
```bash
curl -X POST http://localhost:4096/tui/execute-command \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{"command": "/test"}'
```

---

### Documentación

#### GET /doc
```bash
curl http://localhost:4096/doc
```
Especificación OpenAPI 3.1 completa.

---

## Ejemplo: Flujo Completo

```bash
# 1. Verificar salud
HEALTH=$(curl -s http://localhost:4096/global/health)
echo $HEALTH

# 2. Crear sesión
SESSION=$(curl -s -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{"title": "Proyecto API"}')
SESSION_ID=$(echo $SESSION | jq -r '.id')

# 3. Enviar mensaje
curl -X POST "http://localhost:4096/session/$SESSION_ID/message" \
  -H "Content-Type: application/json" \
  -u opencode:password \
  -d '{
    "parts": [{"type": "text", "text": "Dime hola"}]
  }'
```
