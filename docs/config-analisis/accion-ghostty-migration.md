# Plan de Acción: Migración Completa a Ghostty

## 🎯 Objetivo
Consolidar Ghostty como única solución de terminal en todas las plataformas, eliminando iTerm2 y estandarizando la configuración.

## ✅ Estado Actual
- [x] Ghostty instalado y funcionando en macOS
- [x] Configuración básica establecida en `~/.config/ghostty/config`
- [x] Tema Catppuccin Mocha aplicado
- [x] JetBrains Mono Nerd Font configurada

## 📋 Acciones Inmediatas

### Fase 1: Limpieza macOS (Esta semana)

#### 1. Verificar Dependencias
```bash
# Verificar qué usa actualmente iTerm2
lsof | grep iTerm2
ps aux | grep iTerm2

# Revisar scripts que puedan invocar iTerm2
grep -r "iTerm" ~/.config/
grep -r "iterm" ~/bin/ 2>/dev/null
```

**Checklist:**
- [ ] Verificar que ningún script o alias usa iTerm2
- [ ] Revisar launchd/LaunchAgents que lancen iTerm2
- [ ] Verificar integración con otros apps (Raycast, Alfred, etc.)

#### 2. Migrar Configuración Faltante
```bash
# Si hay settings de iTerm2 que quieres preservar
# Revisar:
cat ~/Library/Preferences/com.googlecode.iterm2.plist

# Comparar con Ghostty actual
cat ~/.config/ghostty/config
```

**Checklist:**
- [ ] Revisar keybindings de iTerm2 no migrados
- [ ] Revisar profiles/temas custom
- [ ] Documentar cualquier feature única de iTerm2 que uses

#### 3. Actualizar Defaults del Sistema
```bash
# Hacer Ghostty el terminal por defecto
# En System Settings > Desktop & Dock > Default terminal

# O desde terminal
defaults write com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers -array-add '{LSHandlerContentType=public.unix-executable;LSHandlerRoleAll=com.mitchellh.ghostty;}'
```

**Checklist:**
- [ ] Configurar Ghostty como terminal por defecto del sistema
- [ ] Actualizar hotkeys de sistema para abrir Ghostty
- [ ] Configurar Raycast/Alfred para usar Ghostty

#### 4. Backup y Eliminación
```bash
# Backup de config de iTerm2 (por si acaso)
mkdir -p ~/Backups/iterm2-$(date +%Y%m%d)
cp -R ~/Library/Preferences/com.googlecode.iterm2.plist ~/Backups/iterm2-$(date +%Y%m%d)/
cp -R ~/Library/Application\ Support/iTerm2 ~/Backups/iterm2-$(date +%Y%m%d)/ 2>/dev/null

# Eliminar iTerm2
rm -rf /Applications/iTerm.app
rm -rf ~/Library/Preferences/com.googlecode.iterm2.plist
rm -rf ~/Library/Application\ Support/iTerm2
rm -rf ~/Library/Caches/com.googlecode.iterm2
rm -rf ~/.config/iterm2

# Si instalado via Homebrew
brew uninstall --cask iterm2
```

**Checklist:**
- [ ] Backup completo de configuración de iTerm2
- [ ] Desinstalar iTerm2
- [ ] Limpiar archivos residuales
- [ ] Verificar que nada se rompió

### Fase 2: Optimización Ghostty (Próxima semana)

#### 5. Refinar Configuración
```bash
# Archivo: ~/.config/ghostty/config

# Revisar y optimizar:
# - Keybindings
# - Window management
# - Shell integration
# - Performance settings
```

**Checklist:**
- [ ] Documentar todos los keybindings actuales
- [ ] Optimizar performance (GPU, rendering)
- [ ] Configurar splits si es necesario
- [ ] Ajustar scrollback y memory settings

#### 6. Testing Exhaustivo
**Casos de uso a probar:**
- [ ] Abrir múltiples tabs/windows
- [ ] Copy/paste entre apps
- [ ] Búsqueda en output
- [ ] Shell integration (pwd, command status)
- [ ] Tmux dentro de Ghostty
- [ ] Neovim con imágenes
- [ ] SSH sessions
- [ ] Performance con logs largos

#### 7. Workflow Integration
**Integrar con:**
- [ ] skhd: Hotkey para abrir Ghostty
- [ ] Raycast: Quick commands
- [ ] Scripts: Actualizar shebangs si necesario
- [ ] Yabai: Rules para Ghostty windows

### Fase 3: Preparación Multi-plataforma (2-3 semanas)

#### 8. Versión Linux de Configuración
```bash
# Crear config portable
# ~/.config/ghostty/config

# Conditional settings por OS
# Usar env vars o detectar OS
```

**Checklist:**
- [ ] Identificar settings específicos de macOS
- [ ] Crear template portable
- [ ] Documentar diferencias por plataforma
- [ ] Testing en VM Linux

#### 9. Nix Configuration
```nix
# Agregar Ghostty a nix config
programs.ghostty = {
  enable = true;
  settings = {
    font-family = "JetBrainsMonoNL Nerd Font Mono";
    font-thicken = true;
    font-thicken-strength = 80;
    theme = "catppuccin-mocha";
    window-padding-x = 10;
    window-padding-y = 10;
    copy-on-select = true;
    cursor-style = "block";
    cursor-style-blink = false;
    shell-integration = "zsh";
  };
};
```

**Checklist:**
- [ ] Agregar Ghostty a flake.nix
- [ ] Configuración en Home Manager
- [ ] Testing en macOS con Nix
- [ ] Preparar para Linux deployment

#### 10. Documentación
**Crear/Actualizar:**
- [ ] README para Ghostty setup
- [ ] Guía de migración desde iTerm2
- [ ] Troubleshooting común
- [ ] Comparativa Ghostty vs otras terminals

## 🎁 Beneficios Obtenidos

### ✅ Portabilidad Total
- Una sola configuración para macOS, Linux, Windows (WSL)
- No más sincronización de configs entre terminals diferentes
- Mismo look & feel en todos los dispositivos

### ✅ Simplicidad
- Menos aplicativos que mantener
- Una sola configuración que aprender
- Menos espacio en disco

### ✅ Modernidad
- GPU rendering
- Image support (Neovim, etc.)
- Mejor performance que iTerm2
- Desarrollo activo

### ✅ Consistencia
- Tema Catppuccin en todos lados
- Fuente JetBrains Mono en todos lados
- Comportamiento predecible

## 📊 Métricas de Éxito

- [ ] 0 referencias a iTerm2 en código/scripts
- [ ] Ghostty funciona en 100% de casos de uso
- [ ] Performance igual o mejor que iTerm2
- [ ] Config sincronizada en Git
- [ ] Ready para deploy en Linux/Windows

## 🚨 Rollback Plan

Si algo sale mal:

```bash
# Reinstalar iTerm2
brew install --cask iterm2

# Restaurar config
cp ~/Backups/iterm2-YYYYMMDD/com.googlecode.iterm2.plist ~/Library/Preferences/
cp -R ~/Backups/iterm2-YYYYMMDD/iTerm2 ~/Library/Application\ Support/

# Reabrir iTerm2 y verificar
```

## 📝 Notas

### Diferencias Conocidas Ghostty vs iTerm2

| Feature | iTerm2 | Ghostty | Notas |
|---------|--------|---------|-------|
| GPU Rendering | ⚠️ | ✅ | Ghostty más rápido |
| Image Support | ✅ | ✅ | Ambos soportan |
| Shell Integration | ✅ | ✅ | Sintaxis diferente |
| Tabs | ✅ | ✅ | Ghostty más simple |
| Splits | ✅ | ⚠️ | Usar tmux en Ghostty |
| Themes | ✅ Muchos | ✅ Custom | Catppuccin en ambos |
| Hotkey Window | ✅ | ⚠️ | Configurar con skhd |
| Triggers | ✅ | ❌ | Reemplazar con scripts |

### Features de iTerm2 que Extrañarías

1. **Hotkey Window**: Ghostty no tiene built-in
   - **Solución**: Usar skhd para toggle window
   
2. **Triggers**: Auto-actions en output
   - **Solución**: Scripts de shell o alertas manuales
   
3. **Session Restore**: iTerm2 restaura tabs
   - **Solución**: Tmux con resurrect
   
4. **Advanced Splits**: Grid complex de splits
   - **Solución**: Tmux es mejor para esto anyway

### Configuraciones Recomendadas Extra

```bash
# ~/.config/ghostty/config

# macOS specific (opcional)
macos-non-native-fullscreen = false
macos-option-as-alt = true

# Performance
window-vsync = true
gtk-single-instance = false

# Clipboard
clipboard-read = allow
clipboard-write = allow

# Keybindings (opcional)
keybind = cmd+t=new_tab
keybind = cmd+w=close_surface
keybind = cmd+shift+[=previous_tab
keybind = cmd+shift+]=next_tab
```

## 🔗 Referencias

- [Ghostty Documentation](https://ghostty.org/docs)
- [Ghostty GitHub](https://github.com/mitchellh/ghostty)
- [Configuración actual](~/.config/ghostty/config)
- [Documento 03-ghostty.md](03-ghostty.md)

## 📅 Timeline

| Semana | Fase | Estado |
|--------|------|--------|
| Semana 1 | Limpieza macOS | ⏳ |
| Semana 2 | Optimización | ⏳ |
| Semana 3-4 | Multi-plataforma | ⏳ |

---

**Última Actualización**: 2026-02-02  
**Estado**: 🟡 En Progreso
