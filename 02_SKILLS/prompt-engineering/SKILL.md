---
name: prompt-engineering
description: >-
  Designs, optimizes, and evaluates high-precision LLM prompts, structured JSON schemas,
  few-shot exemplars, and context-window minimization strategies. Use whenever authoring
  system instructions, structuring LLM outputs, or preventing prompt injection.
---

# Prompt Engineering & Context Design Skill

> **Status**: IMPLEMENTED & TESTED (Workspace)  
> **Version**: 1.0.0  
> **Domain**: DOM-02 (Prompt Engineering and Context Engineering)  

---

## 1. Purpose & Scope
This skill governs the systematic authoring, token optimization, and structured output enforcement for all LLM interactions in the MASTER-AI ecosystem. It prevents conversational drift, hallucinations, and injection attacks by enforcing declarative schemas and few-shot calibration.

## 2. When to Use This Skill
- When designing system prompts for subagents or autonomous tasks.
- When configuring LLMs to return strict JSON matching a Pydantic or TypeScript schema.
- When optimizing long-context prompts to reduce token usage and latency.
- When designing defense gates against prompt injection and jailbreak payloads.
- **Do NOT use for**: General software architecture or non-LLM text authoring.

## 3. Required Inputs
- Target foundational model (Gemini 3.8 Flash/Pro, Claude 3.7, GPT-4o).
- Desired output format (free-form markdown vs. strict JSON schema).
- Domain rules, constraints, and negative constraints ("Never do X").

## 4. Execution Workflow

### Step 1: Establish Persona & Context Boundary
Define explicit identity, primary objective, and negative guardrails. Do not rely on polite conversational phrasing.
- State role in the first sentence.
- Specify exact allowed output formats.
- Explicitly state fallback behavior when information is missing.

### Step 2: Implement Structured JSON Schema
When deterministic data is needed, enforce strict JSON:
- Refer to [STRUCTURED_OUTPUTS_GUIDE.md](./references/STRUCTURED_OUTPUTS_GUIDE.md).
- Use few-shot examples from [few_shot_prompt_examples.json](./examples/few_shot_prompt_examples.json).

### Step 3: Token Estimation & Context Window Validation
Validate prompt weight using the token validator script:
```powershell
python 02_SKILLS/prompt-engineering/scripts/validate_prompt_tokens.py --prompt "Your system prompt text here" --max-tokens 4000
```

### Step 4: Verification & Anti-Injection Testing
- [ ] Role is explicitly defined without ambiguity.
- [ ] Output schema is typed (JSON or Markdown headings).
- [ ] Negative constraints are stated clearly ("Do not...").
- [ ] No personal credentials or secrets are embedded in the prompt.
- [ ] Token count falls within target budget.
