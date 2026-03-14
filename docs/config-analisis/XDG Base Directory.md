# Base de Conocimiento para Configuración Personal (Dotfiles) y Estándar XDG

## 1. Filosofía y Estándar XDG Base Directory
El objetivo principal es evitar el "dotfile clutter" (el desorden de archivos ocultos en `$HOME`) y separar la configuración, los datos y la caché para facilitar las copias de seguridad y la portabilidad.

### Variables de Entorno Principales
El estándar define las siguientes ubicaciones predeterminadas si las variables no están definidas:

| Variable | Valor por Defecto | Propósito | Ejemplo de Contenido |
| :--- | :--- | :--- | :--- |
| **`XDG_CONFIG_HOME`** | `$HOME/.config` | Configuración del usuario. | `nvim/init.lua`, `git/config`. |
| **`XDG_DATA_HOME`** | `$HOME/.local/share` | Datos persistentes del usuario. | Fuentes, correos descargados, bases de datos. |
| **`XDG_CACHE_HOME`** | `$HOME/.cache` | Datos no esenciales (se pueden borrar). | Miniaturas, caché de compilación, caché web. |
| **`XDG_STATE_HOME`** | `$HOME/.local/state` | Datos de estado (historial, logs). | `bash_history`, `viminfo`. |
| **`XDG_RUNTIME_DIR`** | `/run/user/$UID` | Archivos volátiles de ejecución (sockets). | Sockets de comunicación, pipes. |

**Notas Críticas:**
*   **`XDG_RUNTIME_DIR`**: Debe tener permisos `0700`, pertenecer al usuario y limpiarse al cerrar la sesión o reiniciar. Generalmente es configurado por `pam_systemd`.
*   **Directorios de Sistema**: `XDG_CONFIG_DIRS` (defecto `/etc/xdg`) y `XDG_DATA_DIRS` (defecto `/usr/local/share:/usr/share`) definen dónde buscar configuraciones predeterminadas si no están en el home del usuario.

---

## 2. Estrategia de Implementación de Variables
Para que todas las aplicaciones (gráficas y de terminal) respeten estas variables, deben definirse lo antes posible en el proceso de inicio de sesión.

### Dónde definir las variables (Jerarquía)
1.  **Nivel Sistema (Recomendado para GUI y consistencia):**
    *   **PAM (`pam_env`):** Editar `/etc/security/pam_env.conf`. Permite definir variables agnósticas al shell que leen los gestores de sesión gráfica (GDM, SDDM).
    *   **Sintaxis PAM:** `XDG_CONFIG_HOME DEFAULT=@{HOME}/.config`.
2.  **Nivel Shell (Login):**
    *   **Bash:** `~/.bash_profile` o `/etc/profile`.
    *   **Zsh:** `~/.zshenv` (se carga en todas las instancias, recomendado para variables de entorno).
    *   **Fish:** Es complicado porque no lee archivos POSIX por defecto. Se recomienda usar `/etc/environment` o definir variables globales en `conf.d/`.

---

## 3. Gestión de Aplicaciones y Migración
No todas las aplicaciones soportan XDG nativamente. Se clasifican en tres categorías:

### A. Soporte Nativo
Aplicaciones modernas que detectan `XDG_CONFIG_HOME` automáticamente.
*   **Git:** Mover `~/.gitconfig` a `$XDG_CONFIG_HOME/git/config`.
*   **Neovim:** Usa nativamente `$XDG_CONFIG_HOME/nvim/init.lua`.
*   **Firefox (Reciente):** Soporte añadido recientemente (v147+). Mover `~/.mozilla` a `$XDG_CONFIG_HOME/mozilla`.

### B. Soporte Parcial (Requiere Variables de Entorno)
Aplicaciones que permiten cambiar sus rutas mediante variables específicas. Define estas en tu perfil de shell (`.zshenv`, `.bash_profile`, `config.fish`).

*   **Zsh:** Define `export ZDOTDIR="$XDG_CONFIG_HOME/zsh"`. Mueve `.zshrc` a esa carpeta.
*   **GnuPG:** `export GNUPGHOME="$XDG_DATA_HOME/gnupg"`. Asegurar permisos `700` en el directorio.
*   **Vim:** Usar `export VIMINIT='let $MYVIMRC="$XDG_CONFIG_HOME/vim/vimrc" | source $MYVIMRC'`.
*   **GTK 2:** `export GTK2_RC_FILES="$XDG_CONFIG_HOME/gtk-2.0/gtkrc"`.
*   **Go (Golang):** `export GOPATH="$XDG_DATA_HOME/go"`.
*   **Wget:** `export WGETRC="$XDG_CONFIG_HOME/wgetrc"`.
*   **Historiales (Bash/Python/Node):** Muchos historiales REPL pueden redirigirse. Ejemplo: `export PYTHON_HISTORY=$XDG_STATE_HOME/python_history` (Python 3.13+).

### C. Hardcoded / Sin Soporte (Soluciones)
Aplicaciones que fuerzan el uso de `$HOME`.
*   **OpenSSH:** Difícil de mover completamente. Se puede usar `alias ssh='ssh -F "$XDG_CONFIG_HOME/ssh/config"'`, pero seguirá buscando claves en `~/.ssh` por defecto.
*   **Wrappers:** Herramientas como `boxxy` interceptan llamadas al sistema para redirigir archivos al vuelo.
*   **Alias de Home:** Truco sucio para comandos simples: `alias wpa_cli='HOME=$XDG_STATE_HOME wpa_cli'`.

---

## 4. Herramientas de Gestión de Dotfiles
Para sincronizar tu configuración entre máquinas, tienes dos enfoques principales documentados.

### Enfoque A: GNU Stow (Enlaces Simbólicos)
Ideal si prefieres mantener la estructura de carpetas manualmente y usar enlaces simbólicos.
*   **Estructura:** Creas una carpeta `~/dotfiles/nvim/.config/nvim/init.lua`.
*   **Comando:** Ejecutas `stow nvim` desde la carpeta `dotfiles`.
*   **Resultado:** Crea un enlace simbólico en `~/.config/nvim/init.lua` apuntando a tu repo.
*   **Ventaja:** Simple, los cambios se reflejan inmediatamente.
*   **Desventaja:** Manejo deficiente de secretos y diferencias entre sistemas operativos.

### Enfoque B: Chezmoi (Plantillas y Generación)
Más potente para entornos complejos o multiplataforma.
*   **Funcionamiento:** No usa enlaces simbólicos por defecto; genera los archivos en el destino basándose en un "estado fuente".
*   **Ventajas:**
    *   **Plantillas:** Puedes usar lógica (`if eq .chezmoi.os "darwin"`) para variar la configuración entre Linux y macOS.
    *   **Secretos:** Integración con gestores de contraseñas (1Password, Bitwarden) para no subir secretos a Git.
    *   **Estado:** Sabe qué archivos borrar o modificar sin romper el sistema.
*   **Flujo:** `chezmoi edit $FILE` -> `chezmoi apply`.

---

## 5. Consideraciones por Shell

### Bash
*   **Inicio:** Lee `/etc/profile`, luego `~/.bash_profile` (login) o `~/.bashrc` (interactivo).
*   **Recomendación:** Exportar variables XDG en `.bash_profile` y luego cargar `.bashrc`.

### Zsh
*   **Inicio:** Lee `~/.zshenv` siempre. Es el lugar ideal para `export XDG_CONFIG_HOME=...` y `ZDOTDIR`.
*   **Limpieza:** Moviendo `ZDOTDIR`, puedes tener `.zshrc`, `.zprofile`, etc., dentro de `.config/zsh/`.

### Fish
*   **Variables:** No es compatible con POSIX. Usa `set -gx VAR valor` para globales.
*   **Universal Vars:** `set -U` persiste entre sesiones pero se guarda en un archivo `fish_variables` que no suele controlarse con versiones (riesgo de exponer rutas absolutas privadas).
*   **Recomendación:** Usar scripts en `~/.config/fish/conf.d/` para definir variables de entorno, en lugar de usar variables universales, para facilitar la portabilidad.

---

## 6. Consideraciones Multiplataforma (macOS y Windows)

### macOS
*   **Estándar Nativo:** Usa `~/Library/Application Support` y `~/Library/Preferences`.
*   **Tendencia CLI:** Herramientas de línea de comandos (Atmos, gh, nvim) están migrando a usar `~/.config` también en macOS para consistencia con Linux.
*   **Adaptación:** Puedes forzar variables XDG en macOS para unificar tus dotfiles con Linux.

### Windows
*   **Equivalencias:**
    *   `XDG_CONFIG_HOME` -> `%APPDATA%` (Roaming).
    *   `XDG_DATA_HOME` -> `%LOCALAPPDATA%`.
*   **Chezmoi en Windows:** Es compatible y útil para manejar las rutas y finales de línea (CRLF vs LF).

---

## 7. Mantenimiento y Auditoría
*   **XDG-Ninja:** Herramienta recomendada para escanear tu `$HOME` y decirte qué archivos están fuera de lugar y cómo moverlos.
*   **Copias de Seguridad:**
    *   Respalda `XDG_CONFIG_HOME` (configuraciones críticas) y `XDG_DATA_HOME` (tus datos).
    *   Excluye `XDG_CACHE_HOME` (se regenera) y `XDG_STATE_HOME` (historiales y logs prescindibles).

### Guía Rápida de Inicio
1.  **Auditoría:** Ejecuta `xdg-ninja` para ver el estado actual.
2.  **Base:** Define las variables XDG en `/etc/security/pam_env.conf` (si tienes acceso root) o en tu `.zshenv`/`.bash_profile`.
3.  **Migración:** Mueve carpetas soportadas (ej. nvim, git) a `~/.config`.
4.  **Gestión:** Inicia un repo con **Chezmoi** (`chezmoi init`) para gestionar los archivos movidos, o usa **Stow** creando la estructura de carpetas.
5.  **Limpieza:** Aplica variables de entorno para aplicaciones rebeldes (ej. `ZDOTDIR`, `GNUPGHOME`).