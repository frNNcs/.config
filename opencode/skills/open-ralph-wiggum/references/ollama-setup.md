# Ollama Setup para Open Ralph Wiggum

Guía de configuración completa para usar Ollama como backend de modelos con Open Ralph Wiggum vía opencode.

---

## Arquitectura

```
ralph CLI
  └── opencode (agente)
        └── Ollama API (http://localhost:11434)
              └── Modelo local (llama3.1, qwen2.5-coder, etc.)
```

---

## 1. Requisitos Previos

```bash
# Verificar Ollama instalado
ollama --version

# Verificar opencode instalado
opencode --version

# Verificar bun instalado (para ralph)
bun --version

# Verificar ralph instalado
ralph --version
```

---

## 2. Configurar opencode con Ollama

opencode usa la configuración en `~/.config/opencode/opencode.json`.

### Via archivo de configuración:

```json
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  },
  "model": "ollama/qwen2.5-coder:7b"
}
```

### Via API del servidor opencode (si está corriendo como servidor):

```bash
curl -X PATCH http://localhost:4096/config \
  -H "Content-Type: application/json" \
  -d '{
    "providers": {
      "ollama": {
        "apiBase": "http://localhost:11434"
      }
    }
  }'
```

---

## 3. Modelos Recomendados para Coding

| Modelo | Tamaño | Uso recomendado |
|---|---|---|
| `qwen2.5-coder:7b` | ~4GB | Coding, razonamiento, tasks medianos |
| `qwen2.5-coder:14b` | ~9GB | Coding de alta calidad, refactoring |
| `llama3.1:8b` | ~4.7GB | Uso general, generación de texto |
| `codellama:13b` | ~7.4GB | Generación y explicación de código |
| `deepseek-coder:6.7b` | ~3.8GB | Código eficiente, completions |
| `mistral:7b` | ~4.1GB | Velocidad + calidad balanceadas |

### Descargar modelos:

```bash
ollama pull qwen2.5-coder:7b
ollama pull llama3.1:8b
ollama pull codellama:13b
```

---

## 4. Verificar Conexión

```bash
# Ollama debe estar corriendo
ollama serve

# Listar modelos disponibles
ollama list

# Test directo de la API
curl http://localhost:11434/api/tags

# Test con opencode
opencode --model ollama/qwen2.5-coder:7b "Hola, di 'listo'"
```

---

## 5. Ejecutar Ralph con Ollama

```bash
# Asegurarse de que ollama está corriendo
ollama serve &

# Loop con modelo local
ralph "Revisa y corrige los errores de TypeScript. Cuando todo compile, responde <promise>COMPLETE</promise>" \
  --agent opencode \
  --model ollama/qwen2.5-coder:7b \
  --max-iterations 10

# Tasks mode con Ollama
ralph --tasks "Implementa sistema de logging" \
  --agent opencode \
  --model ollama/qwen2.5-coder:14b
```

---

## 6. Ollama en Servidor Remoto (192.168.1.40)

El servidor `192.168.1.40` tiene instalados **Ollama**, **opencode** y **ralph**. 

### Conexión SSH

Ya existe una sesión SSH configurada en `~/.ssh/config`:

```ssh-config
Host ollama
    HostName 192.168.1.40
    User root
    IdentityFile ~/.ssh/id_ed25519_ollama
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    Compression yes
    ControlMaster auto
```

### Conectar al servidor

```bash
# Conectar directamente
ssh ollama

# O ejecutar comando remoto
ssh ollama "ollama list"
ssh ollama "ralph --version"
```

### Opción A: Ejecutar ralph directamente en el servidor

```bash
# Conectar y ejecutar ralph en el servidor remoto
ssh ollama "cd /ruta/proyecto && ralph 'Corrige errores de lint' --max-iterations 5"

# O conectar interactivamente
ssh ollama
cd /tu/proyecto
ralph "Tarea..." --max-iterations 10
```

### Opción B: Usar Ollama remoto desde máquina local

Si prefieres usar ralph local pero con el modelo de Ollama del servidor:

```bash
# 1. Crear túnel SSH al puerto de Ollama
ssh -L 11434:localhost:11434 ollama -N &

# 2. Configurar opencode para usar localhost (túnel)
# En ~/.config/opencode/opencode.json:
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  }
}

# 3. Ejecutar ralph local con modelo remoto
ralph "Tarea..." --agent opencode --model ollama/qwen2.5-coder:7b
```

### Opción C: Conexión directa (sin túnel)

Si Ollama está expuesto en la red:

```bash
# En el servidor (192.168.1.40), exponer Ollama
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# Configurar opencode local para apuntar al servidor
# En ~/.config/opencode/opencode.json:
{
  "providers": {
    "ollama": {
      "apiBase": "http://192.168.1.40:11434"
    }
  }
}
```

### Verificar servicios en el servidor

```bash
# Verificar que los servicios están corriendo
ssh ollama "systemctl status ollama || ollama serve &"
ssh ollama "ollama list"
ssh ollama "which ralph && ralph --version"
ssh ollama "which opencode && opencode --version"
```

### Modelos disponibles en 192.168.1.40 (CPU-only)

| Modelo | Tamaño | Tiempo por iteración | Notas |
|--------|--------|---------------------|-------|
| `qwen3.5:0.8b` | 1.0 GB | ~1-2 min | ⚠️ Muy pequeño, puede no seguir instrucciones |
| `llama3.2:1b` | 1.3 GB | ~3-4 min | ⚠️ Puede divagar, no recomendado para coding |
| `llama3.2:3b` | 2.0 GB | ~5-8 min | Mínimo recomendado para tareas simples |
| `qwen2.5-coder:3b` | 1.9 GB | ~4-6 min | ✅ Mejor opción para coding en CPU |

> **Nota:** El servidor 192.168.1.40 usa solo CPU. Modelos ≤1B pueden emitir `<promise>COMPLETE</promise>` prematuramente sin completar la tarea.

### Fix requerido: Symlink de Bun

Si ralph no encuentra bun, crear symlink:

```bash
ssh ollama "ln -sf /root/.bun/bin/bun /usr/local/bin/bun"
```

Esto es necesario porque el wrapper de ralph (`/usr/local/bin/ralph`) busca `bun` en el PATH del sistema, no en `~/.bun/bin/`.

---

## 7. Parámetros de Rendimiento

### Configuración de contexto en Ollama:

```bash
# Aumentar ventana de contexto para tareas de código complejas
OLLAMA_NUM_CTX=8192 ollama serve

# O en Modelfile personalizado:
FROM qwen2.5-coder:7b
PARAMETER num_ctx 8192
PARAMETER temperature 0.1
PARAMETER top_p 0.9
```

Crear y usar Modelfile:

```bash
# Crear modelo optimizado para coding
ollama create ralph-coder -f ./Modelfile

# Usar con ralph
ralph "tarea" --model ollama/ralph-coder
```

---

## 8. Troubleshooting

| Problema | Causa probable | Solución |
|---|---|---|
| `connection refused` en ollama | Ollama no está corriendo | `ollama serve` |
| Modelo no encontrado | Modelo no descargado | `ollama pull <modelo>` |
| opencode no usa Ollama | Config incorrecta | Verificar `~/.config/opencode/opencode.json` |
| Loop muy lento | Modelo muy grande para hardware | Usar modelo más pequeño |
| `<promise>COMPLETE</promise>` nunca aparece | Modelo no sigue instrucciones | Probar `qwen2.5-coder` o `llama3.1` |
| Modelo emite COMPLETE sin hacer nada | Modelo muy pequeño (≤1B) | Usar modelo ≥3B para coding |
| Modelo divaga con explicaciones | Modelo no optimizado para código | Usar `qwen2.5-coder` |
| CUDA out of memory | GPU sin suficiente VRAM | Usar modelo cuantizado (`:q4_0`) |

### Diagnóstico rápido:

```bash
# Ver si ollama está respondiendo
curl -s http://localhost:11434/api/tags | jq '.models[].name'

# Ver logs de ollama
journalctl -u ollama -f   # systemd
# o
ollama logs              # si disponible

# Ver uso de GPU
nvidia-smi               # NVIDIA
# o
watch -n 1 ollama ps     # ver modelos cargados
```

---

## 9. Integración con opencode como Servidor

Si se usa opencode en modo servidor (puerto 4096):

```bash
# Iniciar opencode server
opencode --port 4096 &

# Configurar Ollama vía API
curl -X PATCH http://localhost:4096/config \
  -H "Content-Type: application/json" \
  -d '{"providers": {"ollama": {"apiBase": "http://localhost:11434"}}}'

# Ralph entonces usa el servidor opencode
ralph "tarea" --agent opencode
```
