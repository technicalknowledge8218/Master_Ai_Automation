---
name: story-writing
title: Short-Form & Cinematic Screenwriting
description: Authors structured 4-act screenplays with clear inciting incidents, escalating conflict, motivated twists, and memorable payoffs.
version: 1.0.0
publisher: Master AI Core Architecture
---

# SHORT-FORM & CINEMATIC SCREENWRITING

## 1. PURPOSE & OBJECTIVE
Authors structured 4-act screenplays with clear inciting incidents, escalating conflict, motivated twists, and memorable payoffs.

## 2. WHEN TO USE
Activate this skill whenever a production phase requires execution of the **story-writing** stage in the pipeline manifest.

## 3. REQUIRED INPUTS
- Active project manifest (pipeline_defs/<pipeline>.yaml)
- Prerequisite artifacts from earlier stages (e.g. screenplay, character models, or dialogue timeline)
- Production parameters (duration, target aspect ratio, audio mix target)

## 4. STANDARD WORKFLOW
1. **Preflight Audit**: Verify all required input assets exist and are non-empty.
2. **Context Injection**: Load the current creative mandate and reference guidelines.
3. **Execution**: Execute the task adhering strictly to the established rules and constraints.
4. **Validation Check**: Run automated sanity checks on the output artifact before handing off.

## 5. QUALITY STANDARDS & BEST PRACTICES
- Zero assumptions or loose talk.
- Maintain consistency with the established narrative tone.
- Ensure 9:16 vertical safe zone compliance (280px top, 320px bottom).
- Adhere to the ₹0 /  budget rule.

## 6. FAILURE HANDLING & RECOVERY
- If input asset is missing, halt and request prerequisite generation.
- If output fails validation criteria, enter targeted revision loop (maximum 3 iterations).
