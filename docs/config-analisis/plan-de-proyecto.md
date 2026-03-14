# Plan de Proyecto - Modernización y Portabilidad de Configuraciones

## Objetivo General

Transformar la configuración actual de macOS en un sistema multiplataforma, reproducible y declarativo que funcione en macOS, Linux (Ubuntu) y Windows, utilizando Nix como herramienta de gestión.

## Fases del Proyecto

### Fase 1: Auditoría y Limpieza (1-2 semanas)

#### 1.1 Inventario Completo
- [x] Documentar todos los aplicativos configurados
- [x] Identificar dependencias entre aplicativos
- [x] Mapear archivos de configuración
- [ ] Identificar configuraciones redundantes o obsoletas
- [ ] Documentar configuraciones no sincronizadas

#### 1.2 Limpieza y Organización
- [ ] Eliminar configuraciones no utilizadas
- [ ] Consolidar archivos duplicados
- [ ] Estandarizar nombres de archivos
- [ ] Limpiar cache y temporales
- [ ] Actualizar documentación inline

#### 1.3 Testing Actual
- [ ] Verificar que todas las configuraciones funcionen
- [ ] Documentar bugs conocidos
- [ ] Crear lista de mejoras deseadas
- [ ] Identificar cuellos de botella de performance

### Fase 2: Extracción de Configuración Base (2-3 semanas)

#### 2.1 Separación por Capas
```
Configuración
├── Base (Universal)
│   ├── Shell (zsh/fish configs)
│   ├── Editor (Neovim)
│   ├── Terminal (tmux)
│   ├── Tools (lsd, bat, atuin)
│   └── Themes (Catppuccin)
├── Platform-Specific
│   ├── macOS (yabai, skhd, sketchybar)
│   ├── Linux (i3, polybar, rofi)
│   └── Windows (komorebi, rainmeter)
└── Machine-Specific
    ├── Work
    ├── Personal
    └── Server
```

#### 2.2 Templates y Generators
- [ ] Crear templates base para cada aplicativo
- [ ] Scripts de generación por plataforma
- [ ] Sistema de variables de entorno
- [ ] Configuración por roles (dev, sysadmin, etc.)

#### 2.3 Documentación de Transición
- [x] Mapeo de aplicativos macOS → Linux
- [x] Mapeo de aplicativos macOS → Windows
- [ ] Guías de migración paso a paso
- [ ] Scripts de conversión automática

### Fase 3: Implementación con Nix (3-4 semanas)

#### 3.1 Setup Inicial de Nix

**Estructura Propuesta:**
```
~/.config/nix-config/
├── flake.nix              # Entry point
├── home.nix               # Home Manager config
├── hosts/
│   ├── macbook-pro.nix
│   ├── ubuntu-desktop.nix
│   └── windows-wsl.nix
├── modules/
│   ├── shell/
│   │   ├── zsh.nix
│   │   └── fish.nix
│   ├── editor/
│   │   └── neovim.nix
│   ├── terminal/
│   │   ├── ghostty.nix
│   │   └── tmux.nix
│   ├── window-manager/
│   │   ├── yabai.nix
│   │   ├── i3.nix
│   │   └── sway.nix
│   └── themes/
│       └── catppuccin.nix
├── overlays/
└── lib/
```

#### 3.2 Migración Gradual por Aplicativo

**Prioridad Alta (Core Tools):**
1. [ ] Shell (zsh/fish)
2. [ ] Neovim
3. [ ] Tmux
4. [ ] Shell tools (lsd, bat, atuin)
5. [ ] Git config

**Prioridad Media:**
6. [ ] Ghostty/Terminal config
7. [ ] Development tools (gh, node, python)
8. [ ] Fonts
9. [ ] Themes

**Prioridad Baja:**
10. [ ] Window managers
11. [ ] Status bars
12. [ ] Productivity apps

#### 3.3 Testing en Máquina Virtual
- [ ] Setup VM Ubuntu para testing
- [ ] Setup VM Windows con WSL
- [ ] Scripts de testing automatizado
- [ ] Comparación de resultados

### Fase 4: Portabilidad Linux (Ubuntu) (2-3 semanas)

#### 4.1 Window Management
- [ ] Setup i3-gaps como alternativa a Yabai
- [ ] Migrar keybindings de skhd a i3 config
- [ ] Configurar polybar como alternativa a SketchyBar
- [ ] Tema Catppuccin para todos los componentes

#### 4.2 Desktop Environment
- [ ] Rofi como alternativa a Raycast
- [ ] Configurar compositor (picom)
- [ ] Setup de wallpapers y lockscreen
- [ ] Configurar dunst para notificaciones

#### 4.3 Terminal y Shell
- [ ] Verificar Ghostty en Linux
- [ ] Alternativa: Alacritty o Kitty
- [ ] Configurar fish/zsh
- [ ] Migrar aliases y functions

#### 4.4 Tools y Utilities
- [ ] Verificar lsd, bat, atuin
- [ ] Configurar clipboard manager
- [ ] Setup de screenshot tools
- [ ] Configurar file manager

### Fase 5: Portabilidad Windows (2-3 semanas)

#### 5.1 WSL2 Setup
- [ ] Instalar WSL2 con Ubuntu
- [ ] Reutilizar configuración de Linux
- [ ] Integración con Windows Terminal
- [ ] Setup de X Server (para GUI apps)

#### 5.2 Native Windows Tools
- [ ] Komorebi como window manager
- [ ] AutoHotkey para keybindings
- [ ] PowerToys setup
- [ ] Rainmeter para widgets

#### 5.3 Development Environment
- [ ] WSL2 + VS Code integration
- [ ] Neovim en WSL
- [ ] Git configuration
- [ ] SSH keys management

### Fase 6: CI/CD y Automatización (1-2 semanas)

#### 6.1 Testing Automatizado
- [ ] GitHub Actions para testing
- [ ] Tests de sintaxis de configs
- [ ] Tests de instalación en VMs
- [ ] Linting de configs

#### 6.2 Deployment
- [ ] Script de bootstrap para nuevas máquinas
- [ ] Ansible playbooks (alternativa)
- [ ] Documentación de setup inicial
- [ ] Recovery y rollback procedures

#### 6.3 Monitoring y Mantenimiento
- [ ] Script de health check
- [ ] Auto-update de configs
- [ ] Backup automático
- [ ] Changelog y versioning

### Fase 7: Documentación y Refinamiento (1 semana)

#### 7.1 Documentación Usuario
- [ ] README principal
- [ ] Guías de instalación por plataforma
- [ ] FAQ y troubleshooting
- [ ] Video tutoriales (opcional)

#### 7.2 Documentación Técnica
- [ ] Architecture decision records
- [ ] API documentation (si aplicable)
- [ ] Contributing guidelines
- [ ] Code comments y docstrings

## Evaluación de Nix

### Ventajas de Usar Nix

#### ✅ Pros
1. **Reproducibilidad**: Builds bit-a-bit reproducibles
2. **Declarativo**: Estado del sistema en código
3. **Rollback**: Fácil rollback a versiones anteriores
4. **Multi-usuario**: Múltiples versiones de paquetes sin conflictos
5. **Cross-platform**: Funciona en macOS y Linux
6. **Home Manager**: Gestión declarativa de dotfiles
7. **Flakes**: Sistema moderno de gestión de dependencias
8. **NixOS**: OS completo declarativo (opcional)

#### ❌ Contras
1. **Curva de aprendizaje**: Sintaxis y conceptos nuevos
2. **Documentación**: Puede ser confusa para principiantes
3. **Disk space**: Múltiples versiones ocupan espacio
4. **Build times**: Primera instalación puede ser lenta
5. **Windows**: Solo vía WSL, no nativo
6. **Debugging**: Más complejo que configs tradicionales

### Alternativas a Nix

#### 1. Ansible
- **Pros**: Popular, bien documentado, sintaxis YAML
- **Contras**: No es declarativo puro, más difícil rollback

#### 2. Dotfiles con Stow
- **Pros**: Simple, directo, solo symlinks
- **Contras**: No gestiona paquetes, menos robusto

#### 3. Chezmoi
- **Pros**: Templates, secretos, multi-máquina
- **Contras**: Solo dotfiles, no paquetes

#### 4. Docker/Containers
- **Pros**: Aislamiento, reproducible
- **Contras**: Overhead, no ideal para desktop

### Recomendación: Enfoque Híbrido

```
1. Nix para paquetes y configuraciones principales (Core)
2. Stow o symlinks para configs simples (Optional)
3. Scripts de shell para tareas específicas (Utilities)
4. Ansible para provisioning de máquinas (Infrastructure)
```

## Estructura de Nix Propuesta

### flake.nix
```nix
{
  description = "Francisco's Multi-Platform Configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    darwin = {
      url = "github:lnl7/nix-darwin";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, darwin, ... }:
    let
      # Shared configuration
      sharedModules = [
        ./modules/shell
        ./modules/editor
        ./modules/terminal
        ./modules/themes
      ];
    in
    {
      # macOS configuration
      darwinConfigurations."macbook-pro" = darwin.lib.darwinSystem {
        system = "aarch64-darwin";
        modules = [
          ./hosts/macbook-pro.nix
          home-manager.darwinModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.users.francisco = import ./home.nix;
          }
        ] ++ sharedModules;
      };

      # Linux configuration
      homeConfigurations."francisco@ubuntu" = home-manager.lib.homeManagerConfiguration {
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
        modules = [
          ./hosts/ubuntu-desktop.nix
          ./home.nix
        ] ++ sharedModules;
      };
    };
}
```

### modules/shell/zsh.nix
```nix
{ config, pkgs, ... }:

{
  programs.zsh = {
    enable = true;
    enableCompletion = true;
    autosuggestion.enable = true;
    syntaxHighlighting.enable = true;
    
    shellAliases = {
      ls = "lsd";
      cat = "bat --paging=never --style=plain";
      vim = "nvim";
    };
    
    initExtra = ''
      # Atuin
      eval "$(atuin init zsh)"
      
      # Custom functions
      source ${./functions.zsh}
    '';
  };
  
  home.packages = with pkgs; [
    lsd
    bat
    atuin
  ];
}
```

### modules/editor/neovim.nix
```nix
{ config, pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;
    viAlias = true;
    vimAlias = true;
    
    # Config from ~/.config/nvim
    extraConfig = ''
      luafile ${./init.lua}
    '';
  };
  
  home.packages = with pkgs; [
    ripgrep
    fd
    nodejs
    python3
  ];
  
  # Symlink existing config
  home.file.".config/nvim".source = config.lib.file.mkOutOfStoreSymlink 
    "${config.home.homeDirectory}/.config/nix-config/modules/editor/nvim";
}
```

## Timeline

| Fase | Duración | Dependencias |
|------|----------|--------------|
| 1. Auditoría | 1-2 semanas | - |
| 2. Extracción | 2-3 semanas | Fase 1 |
| 3. Nix Setup | 3-4 semanas | Fase 2 |
| 4. Linux | 2-3 semanas | Fase 3 |
| 5. Windows | 2-3 semanas | Fase 3, 4 |
| 6. CI/CD | 1-2 semanas | Fase 3, 4, 5 |
| 7. Docs | 1 semana | Todas |
| **Total** | **12-18 semanas** | |

## Hitos Principales

### Milestone 1: Configuración Base (Semana 5)
- ✅ Auditoría completa
- ✅ Configs separadas por capa
- ✅ Templates creados

### Milestone 2: Nix MVP (Semana 9)
- Core tools en Nix
- Testing en macOS
- Home Manager configurado

### Milestone 3: Multi-Platform (Semana 14)
- Funcionando en macOS
- Funcionando en Linux
- Funcionando en Windows (WSL)

### Milestone 4: Production Ready (Semana 18)
- CI/CD configurado
- Documentación completa
- Rollout a todas las máquinas

## Riesgos y Mitigaciones

### Riesgo 1: Complejidad de Nix
- **Mitigación**: Empezar simple, migrar gradualmente
- **Plan B**: Usar Ansible como fallback

### Riesgo 2: Incompatibilidades entre Plataformas
- **Mitigación**: Testing extensivo, configs condicionales
- **Plan B**: Mantener configs separadas si necesario

### Riesgo 3: Time Overrun
- **Mitigación**: Priorizar core tools, features opcionales al final
- **Plan B**: Release incremental

### Riesgo 4: Pérdida de Productividad Durante Migración
- **Mitigación**: Mantener config actual funcionando, migrar en paralelo
- **Plan B**: Rollback rápido a config actual

## Recursos Necesarios

### Tiempo
- **Estimado**: 12-18 semanas (part-time)
- **Full-time equivalent**: 6-9 semanas

### Hardware
- Máquina principal (macOS)
- VM Ubuntu para testing
- VM/Máquina Windows (opcional)

### Software
- Nix/NixOS
- Home Manager
- VirtualBox o UTM
- Git

### Conocimiento
- Nix language
- Linux system administration
- Window managers (i3, yabai, etc.)
- Shell scripting

## Métricas de Éxito

1. ✅ **Reproducibilidad**: Nueva máquina setup en < 1 hora
2. ✅ **Portabilidad**: Funciona en macOS, Linux, Windows (WSL)
3. ✅ **Mantenibilidad**: Cambios pueden hacerse en < 30 min
4. ✅ **Documentación**: Cualquier usuario puede seguir las guías
5. ✅ **Testing**: 90%+ de configs tienen tests
6. ✅ **Performance**: No degradación vs. config manual

## Próximos Pasos Inmediatos

### Esta Semana
1. [x] Completar análisis de configuración actual
2. [ ] Crear repo Git para nix-config
3. [ ] Setup básico de Nix en máquina actual
4. [ ] Migrar primera herramienta (lsd) a Nix

### Próximo Mes
5. [ ] Migrar core tools a Nix
6. [ ] Setup VM Ubuntu
7. [ ] Empezar testing en Linux
8. [ ] Documentar diferencias encontradas

---

**Nota**: Este plan es flexible y será ajustado según se encuentren obstáculos o nuevas oportunidades durante la implementación.
