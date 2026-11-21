# FREE COMPUTE AND CLOUD OPTIONS AUDIT
## Legitimate Zero-Cost GPU Compute, Free Tier APIs, Quota Boundaries & Anti-Paywall Policies

**Document Version:** 1.0.0-zero-budget  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\zero-budget\FREE_COMPUTE_AND_CLOUD_OPTIONS.md`  
**Classification:** Cloud Infrastructure & Zero-Cost Compliance Audit  
**Status:** Approved Technical Audit  

---

## 1. STRICT ZERO-COST CLOUD POLICY

Master AI enforces an uncompromising zero-cost compute policy:
1. **Never Enter Credit Cards:** No service that requires billing information or credit card verification for "free trials" is permitted.
2. **Never Rely on Expiring Credits:** Promotional grants (e.g. Google Cloud $300, AWS $100) are classified as temporary and rejected.
3. **Fail-Closed on Quota Exhaustion:** If a free quota is exhausted, the engine stops or routes to a local offline fallback. It never initiates a paid transaction.

---

## 2. EVALUATION & CLASSIFICATION OF COMPUTE OPTIONS

| Platform / Service | Hardware / Model Offered | Pricing Structure | Verification / Billing Required? | Quota Limits & Reset Cycle | Classification & Master AI Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kaggle Notebooks** | 1x NVIDIA Tesla T4 (16GB) or Dual T4 (32GB VRAM) | **100% Free Forever** | Phone verification only (No credit card) | **30 hours per week** (Resets weekly) | **APPROVED: Primary Free Remote GPU** (For Wan 2.1 / CogVideoX batching) |
| **Google AI Studio** | Gemini 2.0 Flash / 1.5 Flash API | **Permanently Free Tier** | Google Account (No billing required) | **15 RPM, 1M TPM, 1,500 RPD** | **APPROVED: Primary Cloud LLM** (For scriptwriting, RAG & JSON parsing) |
| **Groq Cloud** | Llama 3.3 70B / Llama 3.1 8B | **Permanently Free Tier** | Free signup (No billing required) | High speed, generous daily token limit | **APPROVED: Fast Secondary LLM** (For instant routing & storyboard cues) |
| **Hugging Face Spaces** | 2 vCPU, 16 GB RAM (CPU) / ZeroGPU (A10G) | **Free Community Tier** | Free signup (No billing required) | CPU: Unlimited; ZeroGPU: Queue throttled | **APPROVED: Fallback Web Inference** (For image/audio model demos) |
| **Cloudflare Workers AI** | SDXL-Lightning, BGE-Embeddings, Llama 3 | **Permanently Free Tier** | Free Cloudflare account (No credit card) | **10,000 neurons / day** (Resets daily) | **APPROVED: Micro-Task Inference** (For vector embeddings & quick stills) |
| **Google Colab Free** | 1x NVIDIA T4 (Shared) | Free Ad-hoc Tier | Free signup (No billing required) | Session limited (1–4 hrs; unpredictable) | **RESTRICTED: Interactive Manual Only** (Unreliable for headless automation) |
| **GitHub Codespaces** | 2-core Linux VM, 8 GB RAM, 32 GB disk | **Free User Tier** | GitHub Account (No billing required) | **60 core-hours / month** | **APPROVED: CI/CD & Build Validation** |
| **AWS Free Tier** | EC2 t2.micro, S3 5GB | Temporary 12-Month Trial | **Strict Credit Card Required** | Auto-charges on overage | **REJECTED: Severe Paywall Risk** |
| **Google Cloud Trial** | $300 promotional credit | Temporary 90-Day Trial | **Strict Credit Card Required** | Expiring credit; converts to paid | **REJECTED: Temporary Voucher** |
| **Runway / Midjourney** | Proprietary AI video/image | Subscription Only | Credit Card / Paid Only | Trial credits expire | **REJECTED: Paid Service** |

---

## 3. HEADLESS BATCH GPU AUTOMATION VIA KAGGLE API

Kaggle provides 30 hours per week of genuine NVIDIA T4 compute at ₹0 without billing details. Master AI orchestrates Kaggle headlessly:

### 3.1 Headless Kernel Dispatch Workflow
1. **Script Packaging:** The orchestrator writes a self-contained batch script: `kernel_job.py`.
2. **Metadata Generation:** Writes `kernel-metadata.json` specifying `enable_gpu: true`.
3. **Dispatch:** Calls the official `kaggle` CLI:
   ```bash
   kaggle kernels push -p F:\Master AI\00_CORE_SYSTEM\staging\kaggle_job\
   ```
4. **Polling:** Monitors execution state via `kaggle kernels status <username>/job-name`.
5. **Ingestion:** Downloads the rendered video clip via `kaggle kernels output <username>/job-name -p 16_VIDEO_LIBRARY/`.

### 3.2 Weekly Quota Protection
- Master AI tracks GPU runtime in `STATE.json`.
- When weekly consumption reaches 28.0 hours, cloud GPU dispatch halts automatically, reverting to local Blender 3D or Pexels stock.
