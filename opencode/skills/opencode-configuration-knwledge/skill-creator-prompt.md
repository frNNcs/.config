---
title: Skill Creator Prompt
tags:
  - obsidian
  - prompt
  - skills
  - opencode
created: 2026-03-08
source: opencode/skills/skill-development/references/skill-creator-original.md
---

# Prompt: Crear/Conformar un Skill

Usar este prompt cuando se quiera diseñar o refinar un skill, siguiendo la lógica de `skill-creator-original.md`, pero sin empaquetar ni activar nada todavía.

## Prompt reutilizable

```text
Actúa como especialista en diseño de skills.

Objetivo:
Conformar un skill reutilizable y bien estructurado a partir de la necesidad que te comparta.

Restricciones:
- Mantener enfoque en diseño y documentación del skill.
- No empaquetar ni distribuir.
- No activar ni modificar configuración global todavía.
- Entregar resultado en Markdown listo para guardar en Obsidian.

Proceso obligatorio:
1) Entender el alcance con ejemplos concretos de uso (frases reales que disparan el skill).
2) Planificar contenidos reutilizables:
   - scripts/ (si hay tareas repetitivas y determinísticas)
   - references/ (documentación extensa o de dominio)
   - assets/ (plantillas/recursos de salida)
3) Definir estructura mínima del skill.
4) Redactar SKILL.md:
   - Frontmatter con name y description
   - Description en tercera persona: “This skill should be used when...”
   - Cuerpo en estilo imperativo/infinitivo, claro y accionable
   - Incluir cuándo usar el skill y cómo aplicarlo paso a paso
5) Proponer iteraciones (mejoras futuras) sin ejecutar cambios automáticos.

Formato de salida esperado:
- Sección “Resumen del skill”
- Sección “Triggers sugeridos (frases de usuario)”
- Sección “Estructura de carpetas propuesta”
- Sección “Borrador de SKILL.md”
- Sección “Recursos opcionales (scripts/references/assets)”
- Sección “Siguientes pasos (sin ejecutar)”

Contexto del usuario:
{{PEGAR_AQUÍ_CONTEXTO_DEL_PROYECTO}}

Necesidad puntual:
{{PEGAR_AQUÍ_LO_QUE_QUIERES_QUE_HAGA_EL_SKILL}}
```

## Nota

Esta nota está pensada para uso en Obsidian como plantilla de prompt. No realiza cambios por sí sola en la configuración de OpenCode.
