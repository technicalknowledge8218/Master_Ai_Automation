# ADR-001: Adoption of Model Context Protocol (MCP) for Tool Integration

> **Status**: ACCEPTED  
> **Date**: 2026-11-17  
> **Deciders**: Master Architect, Security Auditor  

---

## 1. Context
Autonomous AI agents require external capabilities (database inspection, browser control, terminal execution). Historically, these integrations were implemented via custom bespoke API wrappers, leading to fragmentation and inconsistent error handling.

## 2. Decision
We adopt the **Model Context Protocol (MCP)** specification over standard `stdio` transport as the primary tool interface. Custom tools will expose JSON schemas compliant with MCP v1.

## 3. Alternatives Considered
- Direct Python subprocess wrapper: Rejected due to lack of standard introspection and client decoupling.
- REST API microservices for tools: Rejected due to local transport latency and port management overhead.

## 4. Consequences
- **Positive**: Standardized client-server protocol; interoperable across any MCP-compliant host.
- **Negative**: Requires Node/Python runtime on host; subprocess management overhead.
