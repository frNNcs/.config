# Ralph Wiggum - Prompt Templates

El éxito del "Ralph Wiggum mode" depende críticamente de escribir buenos prompts que definan claramente el criterio de salida (`<promise>COMPLETE</promise>`) y el camino a seguir.

A continuación, se presentan las plantillas oficiales para los casos de uso más comunes, adaptadas para ser ejecutadas con el CLI `ralph`.

---

## 1. Feature Implementation (Implementación de Funcionalidad)

Útil para construir una característica completa desde cero asegurando cobertura de tests y documentación.

**Comando:**
```bash
ralph "Implementa [NOMBRE_DEL_FEATURE].

Requisitos:
- [Requisito 1]
- [Requisito 2]
- [Requisito 3]

Criterios de éxito:
- Todos los requisitos implementados.
- Tests pasando con >80% de cobertura.
- Sin errores de linter.
- Documentación (README o JSDoc) actualizada.

Cuando todo funcione correctamente y cumpla los criterios, responde únicamente con <promise>COMPLETE</promise>." \
  --max-iterations 30
```

---

## 2. TDD Development (Desarrollo Guiado por Pruebas)

Obliga al agente a seguir el ciclo Rojo-Verde-Refactor en cada iteración.

**Comando:**
```bash
ralph "Implementa [NOMBRE_DEL_FEATURE] usando TDD.

Proceso a seguir estrictamente:
1. Escribe un test que falle para el próximo requisito.
2. Implementa el código mínimo necesario para que pase.
3. Ejecuta los tests.
4. Si falla, corrige y reintenta.
5. Refactoriza si es necesario.
6. Repite para todos los requisitos.

Requisitos a implementar:
- [Lista de requisitos]

Cuando todos los tests estén en verde y los requisitos completos, responde con <promise>DONE</promise>." \
  --max-iterations 50 \
  --completion-promise "DONE"
```

---

## 3. Bug Fixing (Resolución de Errores)

Para arreglar un error esquivo donde el agente necesita investigar, reproducir y solucionar de forma segura.

**Comando:**
```bash
ralph "Arregla el siguiente bug: [DESCRIPCIÓN DEL BUG]

Pasos a seguir:
1. Reproduce o identifica la causa raíz del bug.
2. Implementa la solución.
3. Escribe un test de regresión para evitar que vuelva a ocurrir.
4. Verifica que la solución funciona.
5. Asegúrate de no introducir nuevos problemas (ejecuta todos los tests).

Si después de 15 iteraciones no está arreglado:
- Documenta los problemas que bloquean el avance.
- Enumera los enfoques intentados.
- Sugiere alternativas en un archivo debug.md.

Cuando el bug esté resuelto y el test de regresión pase, responde con <promise>FIXED</promise>." \
  --max-iterations 20 \
  --completion-promise "FIXED"
```

---

## 4. Refactoring (Refactorización Segura)

Garantiza que el agente mejore el código sin romper el comportamiento existente.

**Comando:**
```bash
ralph "Refactoriza [COMPONENTE/MÓDULO] con el objetivo de [OBJETIVO: ej. separar responsabilidades, mejorar rendimiento].

Restricciones estrictas:
- Todos los tests existentes DEBEN seguir pasando.
- NO debe haber cambios en el comportamiento externo ni en la API pública.
- Haz commits incrementales si es posible.

Checklist interno a seguir:
- [ ] Verificar que los tests pasan antes de empezar.
- [ ] Aplicar un paso de refactorización.
- [ ] Verificar que los tests siguen pasando.
- [ ] Repetir hasta completar el objetivo.

Cuando la refactorización esté completa y los tests en verde, responde con <promise>REFACTORED</promise>." \
  --max-iterations 25 \
  --completion-promise "REFACTORED"
```

---

## Mejores Prácticas Generales

1. **La Habilidad Crítica:** El éxito de Ralph depende del operador. Los LLMs son espejos de la habilidad para escribir prompts.
2. **Usa siempre `--max-iterations`:** Es tu red de seguridad principal contra loops infinitos en tareas imposibles.
3. **Manejo de Atascos (Stuck Handling):** Instruye al agente sobre qué hacer si falla repetidas veces (ej. documentar el error en un archivo).
4. **Metas Incrementales:** En lugar de pedir "crea un e-commerce", divídelo en "Fase 1: Auth", "Fase 2: Catálogo", etc.