# MASTER-AI Model Context Protocol (MCP) Catalog

> **Protocol Version**: Model Context Protocol (MCP) v1.0  
> **Source Directory**: `07_MCP_AND_TOOLS/`  

---

## 1. Overview & Security Architecture

The **Model Context Protocol (MCP)** provides a secure, standardized mechanism for MASTER-AI agents to interface with external filesystems, databases, browser runtimes, and cloud APIs.

### MCP Operating Rules:
1. **Zero Secret Leakage**: Connection strings, OAuth tokens, and secrets are passed via environment variables, never hardcoded in `mcp_config.json`.
2. **Transport Isolation**: Prefer local `stdio` transports for sandboxed security. Remote SSE transports require TLS 1.3 and mutual token auth.
3. **Explicit Tool Schemas**: Every custom MCP tool exposed to agents must provide a strictly typed JSON schema with parameter descriptions.

---

## 2. Server Registry

| Server Identifier | Transport | Status | Capabilities & Tools Provided |
| :--- | :--- | :--- | :--- |
| `chrome-devtools-mcp` | stdio | Available | Browser DOM inspection, navigation, screenshots, performance traces, console logs |
| `playwright` | stdio | Available | Headless browser automation, form filling, web interactions, visual scraping |
| `cloudrun` | stdio | Available | Google Cloud Run service management, deployment, logs, and monitoring |
| `genkit-mcp-server` | stdio | Available | Firebase Genkit flow inspection, trace analysis, and runtime management |
| `gsd-task-manager` | stdio | Available | Autonomous goal execution, status querying, and blocker resolution |
| `filesystem-mcp` | stdio | Configured | Sandboxed filesystem operations with path restriction to authorized directories |
| `postgres-mcp` | stdio | Planned | Read-only database query execution, schema reflection, and index inspection |
| `github-mcp` | stdio | Planned | Repository operations, pull request automation, issue tracking, and CI logs |

---

## 3. Antigravity MCP Discovery & Registration
In Antigravity, MCP servers can be mounted globally via `~/.gemini/config/mcp_config.json` or discovered via workspace configuration.
MASTER-AI maintains server blueprints in `07_MCP_AND_TOOLS/servers/` and staged manifests in `07_MCP_AND_TOOLS/configs/`.
