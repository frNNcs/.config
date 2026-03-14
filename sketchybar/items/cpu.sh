#!/bin/bash

sketchybar --add item cpu right \
           --set cpu  update_freq=2 \
                      icon=􀧓  \
                      icon.color=$IRIS \
                      background.drawing=off \
                      script="$PLUGIN_DIR/cpu.sh"
