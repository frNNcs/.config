# llmfit CLI Reference

This document contains detailed information about `llmfit` CLI commands and Ollama integration for remote usage.

## Basic CLI Commands

Always append `--json` when running via an agent to parse the output reliably.

*   **List all models ranked by hardware fit:**
    ```bash
    llmfit --cli --json
    ```
*   **Query top 5 models that fit "perfectly" in VRAM/RAM:**
    ```bash
    llmfit fit --perfect -n 5 --json
    ```
*   **Search for specific models by name, provider, or size:**
    ```bash
    llmfit search "llama 8b" --json
    ```
*   **Get detailed information for a specific model:**
    ```bash
    llmfit info "Mistral-7B" --json
    ```
*   **Get top 5 JSON recommendations (useful for agent consumption):**
    ```bash
    llmfit recommend --json --limit 5
    ```
*   **Filter recommendations by specific use case (e.g., coding):**
    ```bash
    llmfit recommend --json --use-case coding --limit 3
    ```
*   **Check the hardware specs `llmfit` has detected on the machine:**
    ```bash
    llmfit system --json
    ```

## Plan Mode
Plan mode estimates the hardware needed for a specific model configuration, rather than asking what fits current hardware.

*   **Generate an estimate for a specific model and context window:**
    ```bash
    llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192 --json
    ```
*   **Generate an estimate specifying a target quantization:**
    ```bash
    llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192 --quant mlx-4bit --json
    ```
*   **Generate a hardware plan to hit a specific Tokens-Per-Second (TPS) target:**
    ```bash
    llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192 --target-tps 25 --json
    ```

## Ollama Integration

`llmfit` natively integrates with Ollama. 
If Ollama is running on the remote node, `llmfit` will detect installed models automatically.

### Remote Ollama Target
If you are running `llmfit` on a central node but want to evaluate or target a different node running Ollama, use the `OLLAMA_HOST` variable:

```bash
OLLAMA_HOST="http://192.168.1.70:11434" llmfit recommend --json
```

## Hardware Overrides
If SSH passthrough, VMs, or broken drivers prevent `llmfit` from detecting the GPU, you can manually override the VRAM:

```bash
# Override with 32 GB VRAM
llmfit --memory=32G fit --perfect -n 5 --json
```

Cap the context length used for memory estimation:
```bash
llmfit --max-context 8192 recommend --json
```
