# Capability Feasibility Evaluation Criteria

> **Reference**: `02_SKILLS/capability-research/references/`  

---

## 1. Feasibility Dimensions
1. **Compute & Hardware**:
   - Lightweight ($<4\text{ GB}$ RAM, CPU only) $\rightarrow$ Fully Achievable locally.
   - Heavy GPU ($>16\text{ GB}$ VRAM, PyTorch/CUDA) $\rightarrow$ Requires dedicated local GPU or external cloud worker.
2. **API Quotas & Financial Cost**:
   - Free / Sanctioned Open Source $\rightarrow$ Level 1 (Immediate).
   - Pay-per-token API with affordable tiers $\rightarrow$ Level 2 (Tracked).
   - Expensive enterprise licenses $\rightarrow$ Level 3 (Requires user business justification).
3. **Legal & Terms of Service Compliance**:
   - Fully open permissive license (MIT, Apache 2.0).
   - Platform TOS limits (e.g., Meta Graph API business verification, X API paywall).
