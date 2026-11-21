# MASTER-AI Known Limitations & Environmental Constraints

> **Status**: Monitored & Documented  
> **Review Cadence**: Continuous  

---

## 1. Runtime & Environmental Limitations

| Constraint Area | Known Limitation | Mitigation Strategy |
| :--- | :--- | :--- |
| **Context Window Limits** | Excessive inlining of docs overflows LLM context | Enforce Antigravity progressive disclosure; store deep guides in `references/` |
| **Antigravity Rule Budget**| Maximum 24KB per rule file; 20,000 token aggregate budget | Keep root `AGENTS.md` concise; modularize detailed domain rules |
| **Network & Sandboxing** | Agents cannot bypass network/proxy or credential checks | Use sanctioned official APIs and authenticated MCP tool bridges |
| **Large Media in Git** | High-resolution video and raw footage will bloat git repository | Store binary video in `16_VIDEO_LIBRARY` with `.gitignore` exclusion and external cloud references |
| **Social API Rate Limits**| YouTube, Instagram, X enforce strict per-hour and per-day quotas | Implement queue schedulers with exponential backoff in `08_AUTOMATION` |
| **Third-Party API Drift** | External web and API endpoints change or deprecate methods | Mandatory `Research Before Implementation` rule before invoking third-party services |

---

## 2. Unresolved Technical Spikes
- **Platform-Specific Social Media Auth**: Instagram Graph API requires Facebook Developer Business Verification for automated posting.
- **Large Video Processing**: Headless video encoding (ffmpeg) requires dedicated GPU resources when generating 4K long-form documentary content.
