# Propuesta de Unificación de Variables de Configuración

## 1. Objetivo
Centralizar todas las "variables mágicas" que actualmente están dispersas en múltiples archivos de configuración (`yabairc`, `ghostty/config`, `tmux.conf`, etc.) en una única fuente de verdad (Source of Truth). Esto facilitará cambios globales de estilo, rutas y preferencias sin necesidad de editar múltiples archivos.

## 2. Estructura de Datos Propuesta (Source of Truth)

Se propone utilizar un archivo estructurado (YAML, JSON o Nix Set) que actúe como base de datos de configuración.

### Archivo Maestro: `config-vars.yaml` (Ejemplo)

```yaml
system:
  user: "francisco"
  fullname: "Francisco"
  email: "francisco@example.com" # Placeholder
  timezone: "America/Santiago" # Placeholder - ajustar según realidad

directories:
  home: "/Users/francisco" # En linux sería /home/francisco
  config: "${home}/.config"
  data_root: "${home}/projects/homelab/DATA"
  syncthing: "${data_root}/syncthing"
  obsidian_vault: "${syncthing}/obsidian"
  screenshots: "${home}/Desktop/Screenshots"
  projects: "${home}/projects"

visual:
  theme:
    name: "catppuccin"
    flavor: "mocha"
    dark_mode: true
    # Paleta de colores base (Catppuccin Mocha)
    colors:
      base: "#1e1e2e"
      mantle: "#181825"
      crust: "#11111b"
      text: "#cdd6f4"
      subtext0: "#a6adc8"
      subtext1: "#bac2de"
      surface0: "#313244"
      surface1: "#45475a"
      surface2: "#585b70"
      overlay0: "#6c7086"
      overlay1: "#7f8497"
      overlay2: "#9399b2"
      blue: "#89b4fa"
      lavender: "#b4befe"
      sapphire: "#74c7ec"
      sky: "#89dceb"
      teal: "#94e2d5"
      green: "#a6e3a1"
      yellow: "#f9e2af"
      peach: "#fab387"
      maroon: "#eba0ac"
      red: "#f38ba8"
      mauve: "#cba6f7"
      pink: "#f5c2e7"
      flamingo: "#f2cdcd"
      rosewater: "#f5e0dc"

  typography:
    font_family: "JetBrainsMonoNL Nerd Font Mono"
    font_family_ui: "Inter" # O la fuente de sistema
    sizes:
      terminal: 13
      editor: 13
      ui_small: 10
      ui_normal: 12
      ui_large: 16

  layout:
    window:
      gap: 12        # Espacio entre ventanas (Yabai/i3)
      padding: 12    # Espacio externo (Yabai/i3)
      radius: 10     # Bordes redondeados
      border_width: 2
    terminal:
      padding_x: 10  # Padding interno terminal (Ghostty/Alacritty)
      padding_y: 10
    bar:
      height: 32     # Altura de barra (SketchyBar/Polybar)
      padding: 10
      font_size: 12

accounts:
  github:
    user: "frNNcs"
  google:
    user: "francisco" # Usar ID o alias, no email completo si es público

applications:
  tmux:
    prefix: "C-Space"
  neovim:
    leader: " " # Space
```

## 3. Estrategia de Implementación

### Fase A: Uso Actual (Scripting)
Crear un script simple en Python o Bash (`tools/get_config.py`) que lea este YAML y devuelva valores, permitiendo usarlo en scripts de shell existentes.

**Ejemplo de uso en shell:**
```bash
# En lugar de hardcodear 12px
WINDOW_GAP=$(python3 tools/get_config.py visual.layout.window.gap)
yabai -m config window_gap $WINDOW_GAP
```

### Fase B: Generación de Archivos (Templates)
Usar un motor de plantillas (como `mustache` o scripts simples) para generar los archivos de configuración finales (`yabairc`, `ghostty/config`, etc.) a partir de templates que usan estas variables.

**Ejemplo Template Ghostty:**
```
font-family = {{ visual.typography.font_family }}
font-size = {{ visual.typography.sizes.terminal }}
window-padding-x = {{ visual.layout.terminal.padding_x }}
theme = {{ visual.theme.name }}-{{ visual.theme.flavor }}
```

### Fase C: Integración con Nix (Futuro)
Cuando se migre a Nix, este archivo YAML puede ser importado directamente como un `Nix Set` o convertido automáticamente. Nix tiene funciones nativas para leer JSON (`builtins.fromJSON`) y existen adaptadores para YAML.

```nix
# Ejemplo conceptual en Nix
{ pkgs, ... }:
let
  configVars = importJSON ./config-vars.json; # O similar
in
{
  programs.ghostty.settings = {
    font-family = configVars.visual.typography.font_family;
    window-padding-x = configVars.visual.layout.terminal.padding_x;
  };
}
```

## 4. Beneficios de la Unificación

1.  **Consistencia Visual**: Asegura que Yabai, Ghostty, SketchyBar y Neovim usen exactamente los mismos valores de padding, colores y fuentes.
2.  **Facilidad de Cambio**: Cambiar el tamaño de fuente o el padding en todo el sistema requiere editar una sola línea.
3.  **Portabilidad**: Las rutas (`directories`) se pueden ajustar dinámicamente según el OS (macOS vs Linux) en el archivo de variables, manteniendo la lógica de los aplicativos intacta.
4.  **Modularidad**: Separa los "datos" de la "lógica" de configuración.
