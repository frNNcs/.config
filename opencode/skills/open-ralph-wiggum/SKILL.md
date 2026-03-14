---
name: open-ralph-wiggum
description: This skill should be used when the user asks to "usar ralph wiggum", "ejecutar ralph", "loop de agente", "modo tareas ralph", "iterar con IA en mi código", "ralph con ollama", "usar ralph con opencode", "automatizar iteraciones de agente", "ralph --rotation", "ralph tasks mode", "ver estado de ralph", "ralph status", "inyectar contexto a ralph", o cuando necesite configurar, ejecutar o monitorear el orquestador autónomo Open Ralph Wiggum con cualquier agente (opencode, claude-code, codex) y cualquier modelo (Ollama, Claude, etc).
version: 0.1.0
---

# open-ralph-wiggum Skill

Orquestador autónomo de agentes de código mediante el "Ralph Wiggum Technique": loop persistente que repite un prompt sobre el mismo codebase hasta detectar una promesa de completitud.

## Propósito

Open Ralph Wiggum envuelve agentes de codificación (opencode, claude-code, codex, copilot) en un loop de retroalimentación. En cada iteración el agente modifica el código; el mismo prompt aplicado al nuevo estado produce mejoras progresivas hasta que el output contiene `<promise>COMPLETE</promise>`.

Para conectar con Ollama local, configurar opencode como agente de fondo y gestionar modelos locales, ver **`references/ollama-setup.md`**.

---

## Instalación

```bash
# Vía npm
npm install -g @th0rgal/ralph-wiggum

# Vía bun (recomendado)
bun add -g @th0rgal/ralph-wiggum

# Verificar
ralph --version
```

**Requisito:** Runtime [Bun](https://bun.sh/) instalado.

---

## Uso Rápido

```bash
# Prompt básico (agente: opencode por defecto)
ralph "Arregla todos los errores de TypeScript y asegúrate de que los tests pasen"

# Con límite de iteraciones (safety net)
ralph "Implementa autenticación JWT" --max-iterations 15

# Con agente específico
ralph "Refactoriza el módulo de pagos" --agent claude-code

# Con modelo Ollama
ralph "Añade tests unitarios" --agent opencode --model ollama/llama3.1
```

El loop continúa hasta que el agente emita `<promise>COMPLETE</promise>` o se alcance `--max-iterations`.

---

## Casos de Uso Principales

### Caso 1: Loop Simple (fix bugs / implementar feature)

```bash
ralph "Revisa el código, corrige todos los linting errors y asegúrate de que npm test pase. Cuando todo esté correcto, responde con <promise>COMPLETE</promise>"
```

### Caso 2: Tasks Mode (proyecto grande)

Divide el trabajo en un checklist gestionado en `.ralph/ralph-tasks.md`:

```bash
ralph --tasks "Construye una API REST con autenticación, CRUD de usuarios y tests de integración"
```

Ralph genera y sigue el checklist automáticamente, marcando tareas completadas en cada iteración.

### Caso 3: Monitoreo en Tiempo Real

Abrir en terminal separada mientras corre el loop principal:

```bash
ralph --status
```

Muestra: iteraciones actuales, historial, struggle indicators (alertas si el agente está atascado).

### Caso 4: Inyección de Contexto Mid-Loop

Sin detener el proceso en curso, inyectar una pista:

```bash
ralph --add-context "El bug está en src/auth/middleware.ts línea 42, el token no se valida correctamente"
```

Se guarda en `.ralph/ralph-context.md` y se incorpora en la próxima iteración.

### Caso 5: Rotation de Agentes/Modelos

Alternar entre agentes o modelos por iteración para diversificar enfoques:

```bash
ralph "Optimiza el rendimiento" --rotation "opencode:ollama/llama3.1,claude-code:sonnet"
```

Útil para evitar que un solo modelo se estanque en el mismo error.

### Caso 6: Con Ollama Local

```bash
# Asegurarse de que Ollama está corriendo
ollama serve

# Ejecutar ralph con modelo local
ralph "Documenta todas las funciones públicas" --agent opencode --model ollama/qwen2.5-coder:7b

# Ver modelos disponibles
ollama list
```

Para configuración completa de Ollama con opencode, consultar **`references/ollama-setup.md`**.

---

## Archivos de Estado del Proyecto

Ralph crea una carpeta `.ralph/` en el directorio del proyecto:

| Archivo | Propósito |
|---|---|
| `ralph-loop.state.json` | Estado actual del loop activo |
| `ralph-history.json` | Métricas detalladas de iteraciones pasadas |
| `ralph-tasks.md` | Checklist en Tasks Mode |
| `ralph-context.md` | Cola de hints inyectados mid-loop |

---

## Configuración Global

### Agentes personalizados: `~/.config/open-ralph-wiggum/agents.json`

```json
{
  "my-local-agent": {
    "binary": "/usr/local/bin/opencode",
    "args": ["--model", "ollama/llama3.1"]
  }
}
```

### Variables de entorno clave

| Variable | Descripción |
|---|---|
| `RALPH_OPENCODE_BINARY` | Path al binario de opencode |
| `RALPH_CLAUDE_BINARY` | Path al binario de claude-code |

---

## Prompts Efectivos para el Loop

Para que Ralph funcione bien, el prompt **debe incluir la condición de completitud**:

```
"[Tarea concreta]. Cuando hayas terminado y todo funcione correctamente, 
responde únicamente con <promise>COMPLETE</promise>"
```

**Buenas prácticas:**
- Ser específico sobre criterios de éxito (tests en verde, sin errores de lint)
- Incluir qué NO cambiar si hay áreas sensibles
- Con `--max-iterations`, poner un valor 2-3x mayor que el esperado

---

## Tabla de Flags Completa

| Flag | Descripción | Ejemplo |
|---|---|---|
| `--agent` | Agente a usar | `--agent claude-code` |
| `--model` | Modelo específico | `--model ollama/llama3.1` |
| `--max-iterations` | Límite de seguridad | `--max-iterations 20` |
| `--tasks` / `-t` | Modo tareas con checklist | `--tasks "descripción"` |
| `--status` | Dashboard en terminal separada | `ralph --status` |
| `--add-context` | Inyectar hint mid-loop | `--add-context "pista"` |
| `--rotation` | Rotar agentes/modelos | `--rotation "a:m1,b:m2"` |

---

## Recursos Adicionales

### Reference Files

- **`references/templates.md`** — Colección de plantillas de prompts efectivas para Feature Implementation, TDD, Bug Fixing y Refactoring
- **`references/ollama-setup.md`** — Configuración detallada de Ollama como backend, conexión al servidor remoto (192.168.1.40), modelos recomendados
- **`examples/agents.json`** — Archivo de ejemplo con configuraciones personalizadas de agentes (opencode, claude-code, modelos locales)
- **`examples/test-minimal.md`** — Caso de prueba mínimo para verificar el entorno sin estresar el servidor
- **`scripts/check-ralph.sh`** — Verifica que ralph, bun y ollama estén instalados y operativos

### Scripts

- **`scripts/check-ralph.sh`** — Diagnóstico rápido del entorno
