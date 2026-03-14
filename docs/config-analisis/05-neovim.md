# Neovim - Editor de Texto

## Descripción General
Neovim es un editor de texto altamente extensible basado en Vim, con soporte para LSP, tree-sitter y plugins modernos.

## Estado Actual
- **Ubicación**: `~/.config/nvim/`
- **Archivo Principal**: `init.lua`
- **Plugin Manager**: lazy.nvim
- **Plugins**: `~/.config/nvim/lua/plugins/*.lua`
- **Estado**: ✅ Configurado y funcional

## Configuración Actual

### Bootstrap de lazy.nvim
```lua
local lazypath = vim.fn.stdpath('data') .. '/site/pack/lazy/opt/lazy.nvim'
```

### Leaders
```lua
vim.g.mapleader = ' '           -- Space
vim.g.maplocalleader = '\\'     -- Backslash
```

### UI Básico
```lua
termguicolors = true
background = 'dark'
showmode = false
ruler = false
showcmd = false
cmdheight = 0
```

### Sistema de Plugins
```lua
require('lazy').setup({
    spec = {
        { import = "plugins" },  -- Importa desde lua/plugins/*.lua
    },
})
```

## Estructura de Archivos
```
~/.config/nvim/
├── init.lua               # Config principal
├── lazy-lock.json         # Lock file de plugins
├── README-images.md       # Documentación de imágenes
└── lua/
    └── plugins/           # Plugins individuales
        ├── (archivos de configuración de plugins)
```

## Integración con Otros Aplicativos
- **Tmux**: Soporte para imágenes via passthrough
- **Ghostty**: Terminal con soporte de imágenes
- **LSP**: Language Server Protocol para autocompletado
- **Tree-sitter**: Syntax highlighting avanzado
- **Telescope**: Fuzzy finder (probable)
- **Catppuccin**: Tema consistente (probable)

## Dependencias
```bash
# Instalación
brew install neovim

# Dependencias comunes (probables)
brew install ripgrep       # Para telescope
brew install fd            # Para telescope
brew install node          # Para LSP servers
brew install python3       # Para providers
```

## Portabilidad

### ✅ Portabilidad a Linux
- **100% Compatible**: Configuración idéntica
- Sin cambios necesarios en config
- Mismos plugins funcionan

### ✅ Portabilidad a Windows
- **Compatible con adaptaciones**:
  - Paths en Windows: `~/AppData/Local/nvim/`
  - Usar backslashes o forward slashes
  - Verificar disponibilidad de herramientas (ripgrep, fd, etc.)

## Recomendaciones

### Para Multiplataforma
1. **Configuración única**: Lua es cross-platform
2. **Paths relativos**: Usar `stdpath()` para portabilidad
3. **Condicionales por OS**:
```lua
if vim.fn.has('mac') == 1 then
    -- macOS specific
elseif vim.fn.has('unix') == 1 then
    -- Linux specific
elseif vim.fn.has('win32') == 1 then
    -- Windows specific
end
```

### Para Nix
```nix
{
  programs.neovim = {
    enable = true;
    defaultEditor = true;
    viAlias = true;
    vimAlias = true;
    
    plugins = with pkgs.vimPlugins; [
      # Plugins se pueden definir aquí o usar lazy.nvim
    ];
    
    extraLuaConfig = ''
      -- Config se puede poner aquí o cargar desde archivos
    '';
  };
  
  # Herramientas necesarias
  environment.systemPackages = with pkgs; [
    ripgrep
    fd
    nodejs
    python3
  ];
}
```

## Listado de Transición

### Paths por Sistema Operativo
| Tipo | macOS | Linux | Windows |
|------|-------|-------|---------|
| Config | `~/.config/nvim/` | `~/.config/nvim/` | `~/AppData/Local/nvim/` |
| Data | `~/.local/share/nvim/` | `~/.local/share/nvim/` | `~/AppData/Local/nvim-data/` |
| Cache | `~/.cache/nvim/` | `~/.cache/nvim/` | `~/AppData/Local/Temp/nvim/` |

### Plugin Manager Portability
| Manager | macOS | Linux | Windows | Notas |
|---------|-------|-------|---------|-------|
| lazy.nvim | ✅ | ✅ | ✅ | 100% portable |
| packer.nvim | ✅ | ✅ | ✅ | Alternativa |
| vim-plug | ✅ | ✅ | ✅ | Alternativa |

## Plugins Comunes Recomendados

### Esenciales (Probablemente Instalados)
```lua
-- lua/plugins/essentials.lua
return {
    -- Theme
    { "catppuccin/nvim", name = "catppuccin", priority = 1000 },
    
    -- Fuzzy Finder
    { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
    
    -- LSP
    { "neovim/nvim-lspconfig" },
    { "williamboman/mason.nvim" },
    { "williamboman/mason-lspconfig.nvim" },
    
    -- Autocompletion
    { "hrsh7th/nvim-cmp" },
    { "hrsh7th/cmp-nvim-lsp" },
    
    -- Tree-sitter
    { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
    
    -- File explorer
    { "nvim-tree/nvim-tree.lua" },
    
    -- Status line
    { "nvim-lualine/lualine.nvim" },
    
    -- Git
    { "lewis6991/gitsigns.nvim" },
}
```

## Features Destacables
1. **Lua Configuration**: Config moderna en Lua
2. **lazy.nvim**: Plugin manager rápido y eficiente
3. **LSP Native**: Soporte nativo de LSP
4. **Tree-sitter**: Syntax highlighting avanzado
5. **Async**: Operaciones asíncronas
6. **Image Support**: Soporte de imágenes (con terminal adecuado)

## Comandos Esenciales
```vim
" Plugin Management
:Lazy                   " Abrir lazy.nvim UI
:Lazy install          " Instalar plugins
:Lazy update           " Actualizar plugins
:Lazy clean            " Limpiar plugins no usados

" Leaders
<Space>                " Leader key
\                      " Local leader

" Probables keybindings (depende de plugins)
<Space>ff              " Find files (Telescope)
<Space>fg              " Find grep (Telescope)
<Space>e               " File explorer
<Space>gg              " Git (Lazygit/Neogit)
```

## Workflow de Desarrollo

### Setup en Nueva Máquina
```bash
# 1. Instalar Neovim
brew install neovim  # o apt/pacman/etc

# 2. Clonar config
git clone <repo> ~/.config/nvim

# 3. Abrir Neovim (lazy.nvim auto-instala plugins)
nvim

# 4. (Opcional) Instalar LSP servers
:Mason
```

### Mantener Actualizado
```bash
# Actualizar plugins
:Lazy update

# Actualizar tree-sitter parsers
:TSUpdate

# Actualizar LSP servers
:Mason
```

## Integración con Workflow
1. **Editor Principal**: Para código, config files, markdown
2. **Git Integration**: Gitsigns, fugitive o similar
3. **Terminal Integration**: Terminal embebido o toggle term
4. **Project Management**: Telescope para navigation
5. **LSP**: Autocompletado y diagnostics

## Extensiones Recomendadas para Crossplatform

### LSP Servers (Mason)
```
typescript-language-server
lua-language-server
pyright
rust-analyzer
gopls
```

### Formatters
```
prettier
stylua
black
rustfmt
```

## Estado de Sincronización
- **Repositorio Git**: frNNcs/.config (branch: main)
- **Syncthing**: Config sincronizado
- **Plugins**: Se instalan localmente via lazy.nvim
- **Lock File**: `lazy-lock.json` asegura versiones consistentes

## Notas Especiales
- **README-images.md**: Documentación sobre soporte de imágenes en Neovim
- **Backup automático**: El init.lua menciona backups previos
- **Minimal Config**: Config minimalista con lazy.nvim como base
