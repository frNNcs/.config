# Caso de Prueba Mínimo - Ralph Wiggum

Prueba rápida para verificar que el skill funciona sin estresar el servidor.

## Nota sobre rendimiento

El servidor `192.168.1.40` corre Ollama **solo en CPU** (sin GPU), lo cual resulta en tiempos de respuesta de 1-3 minutos por iteración incluso con modelos pequeños.

**Modelos recomendados para pruebas rápidas (CPU-only):**
- `qwen3.5:0.8b` (~1GB) - El más rápido
- `llama3.2:1b` (~1.3GB) - Rápido pero limitado

**Para producción:** Considerar usar GPU o conectar a un servidor con CUDA.

---

## Pre-requisitos

```bash
# Verificar conexión SSH al servidor
ssh ollama "echo 'Conexión OK'"

# Verificar servicios en el servidor
ssh ollama "ollama list && ralph --version"
```

---

## Test 1: Verificación de Entorno (sin loop)

Solo verifica que ralph responde correctamente:

```bash
ssh ollama "ralph --help"
```

---

## Test 2: Loop Mínimo (1 iteración)

Crear un archivo trivial y pedir que lo "complete":

```bash
# Crear directorio de prueba en el servidor
ssh ollama "mkdir -p /tmp/ralph-test && cd /tmp/ralph-test && echo 'const x = 1' > test.ts"

# Ejecutar ralph con 1 sola iteración
ssh ollama "cd /tmp/ralph-test && ralph 'El archivo test.ts ya está correcto. Responde <promise>COMPLETE</promise>' --max-iterations 1"
```

**Resultado esperado:** Ralph detecta la promesa de completitud en la primera iteración y termina.

---

## Test 3: Loop con 2 Iteraciones (verificación de autocorrección)

```bash
# Crear archivo con error simple
ssh ollama "cd /tmp/ralph-test && echo 'const x: string = 123' > error.ts"

# Ralph debe corregir el tipo
ssh ollama "cd /tmp/ralph-test && ralph 'Corrige el error de TypeScript en error.ts. Cuando compile sin errores, responde <promise>COMPLETE</promise>' --max-iterations 3 --model ollama/qwen2.5-coder:7b"
```

**Resultado esperado:** Ralph corrige `const x: string = 123` → `const x: number = 123` (o similar) y emite COMPLETE.

---

## Test 4: Verificar Estado

En una terminal separada mientras corre un loop:

```bash
ssh ollama "cd /tmp/ralph-test && ralph --status"
```

---

## Test 5: Inyección de Contexto

Mientras corre un loop, inyectar una pista:

```bash
ssh ollama "cd /tmp/ralph-test && ralph --add-context 'El tipo correcto es number, no string'"
```

---

## Limpieza

```bash
ssh ollama "rm -rf /tmp/ralph-test"
```

---

## Checklist de Validación

- [x] `ssh ollama` conecta correctamente
- [x] `ralph --version` muestra versión (1.2.2)
- [x] `bun --version` funciona (1.3.10, en `/root/.bun/bin`)
- [x] Ollama responde con modelos listados
- [x] Modelos configurados en opencode: `qwen2.5-coder:3b`, `llama3.2:1b`, `llama3.2:3b`, `qwen3.5:0.8b`
- [ ] Loop con `--max-iterations 1` termina (requiere ~2-3 min en CPU)
- [ ] Loop detecta `<promise>COMPLETE</promise>` y sale
- [ ] `ralph --status` muestra estado

## Configuración aplicada

**PATH de Bun** agregado a `~/.bashrc`:
```bash
export PATH="$PATH:/root/.bun/bin"
```

**opencode config** en `~/.config/opencode/opencode.json`:
```json
{
  "provider": {
    "ollama": {
      "models": {
        "qwen2.5-coder:3b": { "_launch": true, "name": "qwen2.5-coder:3b" },
        "llama3.2:1b": { "name": "llama3.2:1b" },
        "llama3.2:3b": { "name": "llama3.2:3b" },
        "qwen3.5:0.8b": { "name": "qwen3.5:0.8b" }
      },
      "name": "Ollama",
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://127.0.0.1:11434/v1" }
    }
  }
}
```
