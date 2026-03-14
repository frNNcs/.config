# Future Tasks

- [ ] **Deshabilitar SIP (System Integrity Protection)**
    - *Objetivo:* Habilitar todas las funciones avanzadas de `yabai` (cambio instantáneo de espacios, eliminación de sombras, transparencia, sticky windows).
    - *Pasos:*
        1. Reiniciar en modo recuperación (Hold Power button on startup for M1/M2/M3, Cmd+R for Intel).
        2. Abrir Terminal.
        3. Ejecutar: `csrutil disable --with kext --with dtrace --with nvram --with basesystem` (O simplemente `csrutil disable` si no te importan los argumentos específicos, aunque para yabai a veces se recomienda específico para `fs` y `debug`).
        4. *Alternativa recomendada para Yabai:* `csrutil disable --with kext --with dtrace --with nvram --with basesystem` (deja algunas protecciones activas) o configurar `csrutil enable --without fs --without debug`.
        5. Reiniciar.
        6. Instalar Scripting Addition: `sudo yabai --install-sa`
        7. Cargar Scripting Addition: `sudo yabai --load-sa`
