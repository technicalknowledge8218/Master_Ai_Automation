---
name: video-editing
description: Autonomous production engine for viral 2D character explainer reels (Instagram Reels, YouTube Shorts, TikTok) in Master AI. Integrates an interactive 3-step Grill-Me interview, pure Devanagari native Hindi scriptwriting, Voice Vault auto-failover, decoupled mouth 2D character rigging, and zero-overflow kinetic typography.
---

# Master AI Autonomous Video Production Engine (`/video-editing`)

This skill empowers Antigravity to act as a full-cycle automated creative director and technical video renderer. It guides the creation of viral 9:16 vertical reels (1080x1920) featuring animated 2D character hosts, crisp native Indian Hindi voiceovers, and dynamic word-level subtitles.

---

## 1. The Interactive Grill-Me Protocol

When the user triggers `/video-editing` or asks to produce a video, do **NOT** immediately output a generic video without user direction. First, ask 3 concise, high-impact alignment questions using the `ask_question` tool or structured interactive questions:

1. **Topic / Core Hook**:
   - What tech, product, or news story are we covering? (e.g., "Claude Code on Mobile via Termux", "AI Voice Clone Scam", "DeepSeek-V3 vs GPT-4o")
2. **Character Format / Archetype**:
   - **Dev Solo** (Tech Creator / Solo Explainer)
   - **Dev & Neha Duo** (Interactive debate / banter format)
   - **Dr. Kabir** (Senior Tech Mentor / Serious analysis)
   - **Arjun** (Young energetic builder)
3. **Call to Action (CTA)**:
   - What is the final hook? (e.g., "Comment TERMUX for the setup guide", "Follow Zovron Technologies for daily AI workflows", "Link in bio")

Once answered, execute the end-to-end autonomous pipeline without interrupting the user.

---

## 2. Scriptwriting Engine (Devanagari Phonetics)

To guarantee 100% natural Indian pronunciation from TTS engines (Sarvam AI / Gemini TTS), **all spoken scripts must be written in pure Devanagari Hindi phonetics**, even for English technical terms.

### Phonetic Conversion Dictionary:
- "Termux" $\to$ **टर्मक्स**
- "Node.js" $\to$ **नोड जेएस**
- "Claude Code" $\to$ **क्लॉड कोड**
- "Python" $\to$ **पायथन**
- "Command" $\to$ **कमांड**
- "Terminal" $\to$ **टर्मिनल**
- "AI" $\to$ **एआई**
- "Update" $\to$ **अपडेट**
- "Install" $\to$ **इन्स्टॉल**
- "Ready" $\to$ **रेडी**

---

## 3. Multi-Provider Voice Vault Execution

Voice synthesis is routed through `F:\Master AI\00_CORE_SYSTEM\engine\tts\voice_vault.py`:
- **Primary Engine**: Sarvam AI (`bulbul:v3`)
  - Female: `speaker: "neha"`
  - Male: `speaker: "aditya"`
- **Secondary Auto-Failover**: Google Gemini TTS (`gemini-3.8-flash-tts`)
- **Offline Fallback**: Kokoro ONNX (`kokoro-v0_19.onnx`).
- **Strict Rule**: Microsoft Edge-TTS is permanently deleted and strictly forbidden.

---

## 4. Locked 2D Character Rigging & Animation Standard

- **Character Asset Directory**: `F:\Master AI\CHARACTER_LIBRARY`
- **Decoupled Viseme Layering**:
  - Base body & face remain static.
  - Viseme layer swaps dynamically during speech (`REST`, `HALF`, `OPEN`).
  - Natural biological eye blinks (100ms duration every 3.8 to 4.5 seconds).

---

## 5. Kinetic Typography & Zero-Overflow Subtitles

1. **Dual-Line Dynamic Wrapping**: Max 4 words per line.
2. **Safe Margins**: 35px safety padding from screen borders.
3. **Word Pop**: Current word highlighted in `#FFD700` Gold with +25% scale punch.

---

## 6. Execution Command

```bash
python "F:\Master AI\00_CORE_SYSTEM\engine\video_production\render_master_reel.py" --topic "YOUR_TOPIC" --character dev --cta "FOLLOW"
```
