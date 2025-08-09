#!/bin/bash

# Script para auto-aplicar Spicetify después de reinicios
# Colócalo en tu directorio de Spicetify para uso fácil

echo "🎵 Verificando estado de Spicetify..."

# Verificar si Spicetify está aplicado
if ! spicetify config | grep -q "version"; then
    echo "❌ Spicetify no está configurado. Ejecutando backup y apply..."
    spicetify backup apply
else
    echo "✅ Spicetify ya está configurado. Aplicando cambios..."
    spicetify apply
fi

# Bloquear actualizaciones de Spotify
echo "🔒 Bloqueando actualizaciones automáticas de Spotify..."
spicetify spotify-updates block

echo "🎉 ¡Spicetify está listo!"
