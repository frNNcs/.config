---
name: llmfit-manager
description: This skill should be used when the user asks to "manage llmfit", "check models for ollama", "plan hardware for model", "restart ollama remotely", or wants to use llmfit over SSH to find, download, or analyze models for their servers.
---

# Skill: llmfit-manager

This skill provides workflows for managing `llmfit` via CLI remotely over SSH. It integrates `llmfit` with Ollama to plan hardware, find models that fit specific remote nodes, download them, and manage the Ollama service.

## Known Infrastructure
The user (Francisco) has the following remote servers available:
- `192.168.1.70`
- `192.168.1.42`
- `192.168.1.45`
- `192.168.1.75` (Raspberry Pi)

## Core Workflows

### 1. Remote Execution via SSH
Execute `llmfit` commands on remote servers using SSH. Always use the `--json` flag for reliable parsing by the agent.
Use the `-o BatchMode=yes` flag to prevent interactive prompts blocking the agent.

```bash
# Example: Check remote system specs
ssh -o BatchMode=yes user@192.168.1.70 "llmfit system --json"
```

### 2. Querying and Planning Models
To evaluate models that could be improved or implemented in Ollama on a specific node:

1. **Check Recommendations:** Find the top models that fit the remote hardware perfectly.
   ```bash
   ssh user@<ip> "llmfit recommend --json --limit 5"
   ```
2. **Plan Hardware for a specific model:** Check if a specific model configuration fits.
   ```bash
   ssh user@<ip> "llmfit plan 'Qwen/Qwen2.5-Coder-7B' --context 8192 --json"
   ```
3. **Audit Current Models:** List currently installed models in Ollama to see what can be upgraded or removed.
   ```bash
   ssh user@<ip> "ollama list"
   ```

### 3. Deploying Models to Ollama
Once a model is identified as a good fit via `llmfit`, deploy it using Ollama.

1. Pull the recommended model via Ollama:
   ```bash
   ssh user@<ip> "ollama pull <model_name>"
   ```
2. Test the model:
   ```bash
   ssh user@<ip> "ollama run <model_name> 'Tell me a joke'"
   ```

### 4. Service Management (Restarting)
To restart Ollama or the `llmfit serve` API on a remote node safely:

1. **Verify State:** Check if Ollama is currently serving requests or if `llmfit` is running.
   ```bash
   ssh user@<ip> "pgrep -a ollama; pgrep -a llmfit"
   ```
2. **Restart Ollama:**
   ```bash
   ssh user@<ip> "sudo systemctl restart ollama"
   ```
3. **Manage llmfit API (Optional):** Start or restart `llmfit serve` in the background if the REST API is needed.
   ```bash
   ssh user@<ip> "pkill llmfit; nohup llmfit serve --host 0.0.0.0 --port 8787 > /tmp/llmfit.log 2>&1 &"
   ```

## Additional Resources

### Reference Files
- **`references/llmfit-cli.md`** - Comprehensive `llmfit` CLI commands and Ollama integration details.

### Scripts
- **`scripts/remote_llmfit.sh`** - Utility script to securely run llmfit commands across the cluster.
