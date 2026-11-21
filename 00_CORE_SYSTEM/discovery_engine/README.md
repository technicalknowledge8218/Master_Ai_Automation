# Capability Discovery Engine

> **Component**: Workspace Discovery & Intelligence System  
> **Location**: `00_CORE_SYSTEM/discovery_engine/`  
> **Script**: `discovery_engine.py`  

---

## 1. Purpose & Capabilities
The Capability Discovery Engine provides autonomous, read-only inspection of the MASTER-AI workspace and the host Antigravity environment.

It performs:
- **Workspace Skill Scanning**: Discovers and validates all `SKILL.md` files in `02_SKILLS/`, verifying YAML frontmatter, directory structure, and link integrity.
- **Agent Specification Scanning**: Inspects all agent JSON definitions in `03_AI_AGENTS/definitions/`, verifying schema validity, allowed tools, and boundary policies.
- **Host MCP Server Auditing**: Reads `%USERPROFILE%\\.gemini\\config\\mcp_config.json` in read-only mode to catalog active external tools without modifying host settings.
- **Gap Analysis**: Compares active workspace capabilities against the 30 master capability domains.

## 2. Usage
```powershell
python 00_CORE_SYSTEM/discovery_engine/discovery_engine.py
```
Output is stored in `00_CORE_SYSTEM/registry/DISCOVERY_REPORT.json`.
