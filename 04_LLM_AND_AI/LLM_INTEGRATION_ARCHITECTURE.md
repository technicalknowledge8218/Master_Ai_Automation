# Master AI LLM Integration Readiness Architecture

## 1. Overview and Core Invariants

The **Master AI LLM Integration Readiness Architecture (LIRA)** defines the technical foundation for integrating Large Language Models into the MASTER AI ecosystem. 

### Absolute Architectural Invariants
1. **Zero Unapproved Paid API Calls**: Under no circumstances may code, agents, or tools execute billable API calls without explicit, verified human authorization.
2. **Fail-Closed Offline Mock Default**: All development, testing, and sandbox runs default to a deterministic offline mock provider (`MockLLMProvider`).
3. **Provider Agnostic**: No agent or subsystem may couple directly to vendor-specific SDKs (e.g. raw OpenAI or Anthropic clients). All calls route through the unified `BaseLLMClient` interface.
4. **Secret-Zero in Prompts & Logs**: Prompts, system messages, and audit logs are sanitized before dispatch and serialization. No API keys or credentials may be logged.
5. **Human Approval Gating**: Any operation that could alter host state, invoke external networks, spend funds, or execute irreversible actions requires explicit human confirmation.

---

## 2. Provider-Independent LLM Interface

```
┌─────────────────────────────────────────────────────────────┐
│                      MASTER AI AGENT                        │
└──────────────────────────────┬──────────────────────────────┘
                               │ LLMRequest
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   UNIFIED LLM GATEWAY                       │
│  - Prompt Hydration        - Budget & Rate Limiting         │
│  - Context Window Trimming - Output Schema Validation        │
│  - Audit Logging           - Security & Safety Screening    │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌──────────────────────────────┐ ┌─────────────────────────────┐
│  OfflineMockProvider (Active)│ │ CloudProviderAdapter (Future│
│  - Deterministic Mocks       │ │  - Gemini / Claude / GPT    │
│  - Zero Network / Zero Cost  │ │  - Gated by Human Approval  │
└──────────────────────────────┘ └─────────────────────────────┘
```

### 2.1 Core Types & Protocols

```python
from typing import Dict, Any, List, Optional, Protocol, Union
from pydantic import BaseModel, Field

class LLMMessage(BaseModel):
    role: str = Field(..., description="system, user, assistant, or tool")
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

class LLMRequest(BaseModel):
    model_id: str
    messages: List[LLMMessage]
    temperature: float = 0.0
    max_tokens: int = 4096
    top_p: float = 1.0
    response_format: Optional[Dict[str, Any]] = None  # JSON schema for structured output
    tools: Optional[List[Dict[str, Any]]] = None      # Tool definitions
    correlation_id: str
    agent_id: str

class LLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float = 0.0

class LLMResponse(BaseModel):
    id: str
    model_id: str
    content: str
    finish_reason: str
    usage: LLMUsage
    latency_ms: float
    tool_calls: Optional[List[Dict[str, Any]]] = None

class BaseLLMClient(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Execute a completion or chat turn."""
        ...
```

---

## 3. Model Capability Metadata Schema

All models supported or evaluated in the ecosystem are cataloged in `04_LLM_AND_AI/models/MODEL_REGISTRY.json`.

### Metadata Schema Attributes
- `model_id`: Canonical unique model identifier (e.g., `gemini-1.5-pro`, `claude-3-5-sonnet`, `offline-mock`).
- `provider`: Vendor name (`Google`, `Anthropic`, `OpenAI`, `Local-Llama`, `Offline-Mock`).
- `context_window_tokens`: Maximum input + output token budget (e.g., 2,097,152 for Gemini 1.5 Pro).
- `max_output_tokens`: Maximum generated tokens per single request.
- `capabilities`: Feature flags (`streaming`, `tool_calling`, `structured_json`, `vision`, `audio`).
- `pricing_per_1m_input_usd`: Cost per million input tokens.
- `pricing_per_1m_output_usd`: Cost per million output tokens.
- `tier`: Classification (`tier_1_flagship`, `tier_2_fast_efficient`, `tier_3_edge_local`, `mock`).
- `allowed_in_offline_sandbox`: Boolean indicating whether model may run without network.

---

## 4. Prompt Templates and Catalog Management

Standardized, versioned prompts are maintained in `04_LLM_AND_AI/prompts/PROMPT_CATALOG.json`.

### Prompt Invariant Rules
1. **Strict Versioning**: Prompts follow semantic versioning (`v1.0.0`). Editing a prompt requires incrementing its minor version.
2. **Template Variables**: Variables use standard mustache syntax `{{variable_name}}`.
3. **No Dynamic Code Injection**: User inputs are parameterized and escaped to prevent prompt injection attacks.
4. **Mandatory Output Contracts**: Every system prompt includes explicit output format expectations (e.g. valid JSON matching a named schema).

---

## 5. Context Window and Token Management

To prevent context exhaustion and runaway costs:
1. **Token Estimation**: Client calculates prompt tokens prior to dispatch using provider tokenizers (`tiktoken` for OpenAI, SentencePiece for LLaMA, Gemini tokenizer).
2. **Sliding Window & Truncation Strategy**:
   - System instructions: **Preserved at 100% priority** (never truncated).
   - Recent conversational turns: Preserved in full.
   - Intermediate trajectory steps: Automatically summarized or evicted when context exceeds 75% of context window limit.
3. **Budget Caps per Agent Task**:
   - Lightweight tasks: Max 8,192 tokens.
   - Code generation / refactoring: Max 32,768 tokens.
   - Comprehensive research: Max 128,000 tokens.

---

## 6. Cost Estimation and Budget Enforcement

```
┌─────────────────────────────────────────────────────────────┐
│                 PRE-REQUEST BUDGET CHECK                    │
├─────────────────────────────────────────────────────────────┤
│  1. Check workspace monthly spend: $0.00 / Limit: $0.00      │
│  2. Check task max cost: $0.00 / Limit: $0.00               │
│  3. IF cost > $0.00 AND approval == False:                 │
│         RAISE BudgetExceededError("Gated by policy")        │
└─────────────────────────────────────────────────────────────┘
```

- **Default Financial Limit**: **\$0.00 USD**. No billable API invocation is permitted without explicit user budget authorization.
- **Circuit Breaker**: If any unexpected network connection or non-zero cost is detected, the LLM Gateway immediately aborts execution and logs a critical security alert.

---

## 7. Evaluation Framework for LLM Outputs

All model outputs are systematically evaluated across four gates before being accepted by the orchestrator:

1. **Gate 1: Schema Compliance**:
   - If structured output requested, validates JSON payload against Pydantic model.
   - Parse errors trigger an automatic retry with repair prompt.
2. **Gate 2: Code Safety & Static Analysis**:
   - Generated code is passed through AST parsers and linters (`ruff`, `eslint`).
   - Forbids dangerous functions (`eval`, `exec`, unescaped raw SQL, subprocess shells).
3. **Gate 3: Semantic Consistency & Grounding**:
   - Cross-references generated citations, file paths, and identifiers against actual workspace files.
4. **Gate 4: Security & Sensitive Content Check**:
   - Scans output for accidental credential leakage, secret tokens, or private host paths.

---

## 8. Audit Logging and Observability

Every LLM transaction produces an immutable JSON log record stored in `04_LLM_AND_AI/audit_logs/`:

```json
{
  "timestamp": "2026-11-17T02:35:00.000Z",
  "correlation_id": "req-98f7-41ab-8812",
  "agent_id": "AGT-003",
  "model_id": "mock-llm-deterministic",
  "provider": "OfflineMockProvider",
  "tokens": {
    "prompt": 128,
    "completion": 45,
    "total": 173
  },
  "cost_usd": 0.0,
  "latency_ms": 12.4,
  "status": "SUCCESS",
  "sanitized_prompt_hash": "sha256-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

## 9. Fail-Closed Offline Mock Implementation

The active provider during Phase 5 is `OfflineMockProvider`. It operates with:
- Zero socket connections (`socket.socket` disallowed).
- Deterministic response fixtures indexed by task type or prompt hash.
- Full compliance with `BaseLLMClient` protocol.
- Instant sub-millisecond response times for regression and unit test suites.
