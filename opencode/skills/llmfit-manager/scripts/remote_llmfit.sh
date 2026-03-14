#!/bin/bash
# Utility script to run llmfit commands on a specific node in the cluster

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <target_ip> <llmfit_command...>"
    echo "Example: $0 192.168.1.70 system --json"
    exit 1
fi

TARGET_IP=$1
shift
COMMAND="llmfit $@"

echo "Executing on $TARGET_IP: $COMMAND"
ssh -o BatchMode=yes -o ConnectTimeout=5 "francisco@$TARGET_IP" "$COMMAND"
