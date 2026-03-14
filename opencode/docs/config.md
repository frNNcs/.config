# Config

Resumen de las opciones de configuración de OpenCode (JSON / JSONC), ubicaciones, esquema y variables.

## Formato

OpenCode acepta archivos JSON y JSONC (JSON con comentarios). Ejemplo:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Theme configuration
  "theme": "opencode",
  "model": "anthropic/claude-sonnet-4-5",
  "autoupdate": true
}
```

## Ubicaciones

Las configuraciones pueden colocarse en distintas ubicaciones y se combinan mediante un "deep merge": las claves conflictivas se sobrescriben por la configuración más posterior, las claves no conflictivas se preservan.

- Global: `~/.config/opencode/opencode.json` — para temas, providers, keybinds, etc.
- Por proyecto: un `opencode.json` en la raíz del proyecto. OpenCode busca en el directorio actual y asciende hasta el Git directory más cercano. Útil para configuraciones específicas del proyecto y seguro para incluir en Git.
- Ruta personalizada: usa la variable de entorno `OPENCODE_CONFIG` para especificar un archivo alternativo. Ejemplo:

```bash
export OPENCODE_CONFIG=/path/to/my/custom-config.json
opencode run "Hello world"
```

- Directorio personalizado: usa `OPENCODE_CONFIG_DIR` para apuntar a un directorio que será buscado como un `.opencode` adicional. Se carga después de la config global y de los directorios `.opencode`, por lo que puede sobrescribirlos.

## Esquema

El esquema JSON está disponible en `https://opencode.ai/config.json`. Tu editor debería poder validarlo y autocompletar en base a él.

### TUI

Opciones para la interfaz de texto (TUI):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "tui": {
    "scroll_speed": 3,
    "scroll_acceleration": { "enabled": true }
  }
}
```

- `scroll_acceleration.enabled` — habilita aceleración de scroll al estilo macOS; tiene prioridad sobre `scroll_speed`.
- `scroll_speed` — multiplicador (por defecto `1`, mínimo `1`); ignorado si `scroll_acceleration.enabled` es `true`.

### Tools

Controla qué herramientas puede usar el LLM:

```json
{ "tools": { "write": false, "bash": false } }
```

### Models

Configura proveedores y modelos:

```json
{
  "provider": {},
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5"
}
```

- `small_model` se usa para tareas ligeras (por ejemplo, generación de títulos). También se admiten modelos locales.

### Themes

```json
{ "theme": "opencode" }
```

### Agents

Define agentes especializados:

```jsonc
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "tools": { "write": false, "edit": false }
    }
  }
}
```

También puedes definir agentes con archivos Markdown en `~/.config/opencode/agent/` o `.opencode/agent/`.

### Default agent

- `default_agent` — agente primario por defecto (por ejemplo, `"plan"`). Debe ser un agente primario; si no existe o es subagente, OpenCode cae a `"build"` con una advertencia. Aplica a TUI, CLI (`opencode run`), app de escritorio y GitHub Action.

### Sharing

Opción `share` con valores: `"manual"` (por defecto), `"auto"`, `"disabled"`.

### Commands

Define comandos reutilizables (plantillas, agente, modelo, descripción):

```jsonc
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    }
  }
}
```

También es posible definir comandos mediante archivos Markdown en `~/.config/opencode/command/` o `.opencode/command/`.

### Keybinds

Configura combinaciones de teclas con la opción `keybinds` (objeto JSON).

### Autoupdate

Controla las actualizaciones automáticas con `autoupdate`. Ejemplos:

```json
{ "autoupdate": false }
{ "autoupdate": "notify" }
```

`"notify"` evita la descarga automática pero notifica si hay nueva versión.

### Formatters

Configura formateadores de código:

```json
{
  "formatter": {
    "prettier": { "disabled": true },
    "custom-prettier": {
      "command": ["npx", "prettier", "--write", "$FILE"],
      "environment": { "NODE_ENV": "development" },
      "extensions": [".js", ".ts", ".jsx", ".tsx"]
    }
  }
}
```

### Permissions

Por defecto OpenCode permite todas las operaciones; usa `permission` para exigir aprobación de operaciones concretas:

```json
{ "permission": { "edit": "ask", "bash": "ask" } }
```

### MCP servers

Configura servidores MCP con `mcp`.

### Instructions

Incluye archivos o patrones glob para instrucciones del modelo:

```json
{ "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", ".cursor/rules/*.md"] }
```

### Disabled providers

Evita que proveedores se carguen aunque tengan credenciales:

```json
{ "disabled_providers": ["openai", "gemini"] }
```

### Enabled providers

Allowlist de proveedores (si está definida, solo los listados se habilitan):

```json
{ "enabled_providers": ["anthropic", "openai"] }
```

Si un proveedor aparece en ambas listas, `disabled_providers` tiene prioridad.

## Variables

Puedes sustituir valores en la configuración usando variables de entorno o el contenido de archivos.

### Variables de entorno

Usa `{env:VARIABLE_NAME}`:

```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": { "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" } }
  }
}
```

Si la variable no existe, se reemplaza por cadena vacía.

### Archivos

Usa `{file:path/to/file}` para insertar el contenido de un archivo:

```json
{
  "instructions": ["./custom-instructions.md"],
  "provider": {
    "openai": { "options": { "apiKey": "{file:~/.secrets/openai-key}" } }
  }
}
```

Las rutas pueden ser relativas al directorio del config o absolutas (`/` o `~`). Útil para mantener secretos o archivos grandes fuera del archivo principal.

## Enlaces útiles

- [Esquema JSON](https://opencode.ai/config.json)
- [Docs (Config)](https://opencode.ai/docs/config/)
- [TUI](https://opencode.ai/docs/tui)
- [Providers](https://opencode.ai/docs/providers)
- [Agents](https://opencode.ai/docs/agents)
- [Commands](https://opencode.ai/docs/commands)
- [Tools](https://opencode.ai/docs/tools)
- [Rules](https://opencode.ai/docs/rules)
