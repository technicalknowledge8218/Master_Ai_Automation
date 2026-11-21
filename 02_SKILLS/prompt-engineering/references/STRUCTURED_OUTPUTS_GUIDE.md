# Structured Outputs & JSON Schema Enforcement Guide

> **Reference**: `02_SKILLS/prompt-engineering/references/`  

---

## 1. Principles of Structured Output
1. **Schema Over Prose**: Whenever an LLM output is ingested by another system, script, or agent, request strict JSON adhering to a validated schema.
2. **Key Minimization**: Keep JSON object keys short and semantic to preserve output tokens.
3. **Enum Constrained Fields**: Use explicit enum choices rather than free-form string statuses (`"status": "APPROVED" | "REJECTED" | "PENDING"`).

## 2. Gemini & OpenAI JSON Mode Best Practices
- Specify `response_mime_type: "application/json"` or `response_schema` in API calls.
- In prompt text, include a 2-line minimal JSON example to calibrate the model's generation distribution.
- Always include error handling with a JSON schema validator (e.g., Pydantic or Zod) to catch parsing failures.
