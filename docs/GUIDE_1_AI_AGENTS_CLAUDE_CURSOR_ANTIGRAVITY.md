# 🤖 Master AI — Guide 1: AI Agents Setup (Claude Code, Cursor & Antigravity)
**Platform**: Master AI powered by Zovron Technologies  
**Target Audience**: Developers, Tech Creators & Builders using AI IDEs  
**Supported Platforms**: Google Antigravity, Claude Code (CLI & Desktop), Cursor AI, GitHub Copilot  

---

## 1. Quick Overview

This guide explains how to install and run Master AI inside autonomous AI environments such as **Antigravity**, **Claude Code**, or **Cursor**. In this mode, the AI itself acts as your creative director, scriptwriter, and rendering engineer via interactive conversational slash commands (e.g., `/video-editing`).

---

## 2. 1-Click Master Prompt (For Any AI Agent)

Simply copy and paste this prompt directly into your **Claude Code**, **Cursor Composer**, or **Antigravity** chat window:

```markdown
You are acting as the Master AI Autonomous Creative Engine powered by Zovron Technologies.
Repository: https://github.com/technicalknowledge8218/Master_Ai_Automation.git

Please execute the following onboarding tasks:
1. Clone the Master AI repository into the current workspace if not present.
2. Verify Python dependencies from `requirements.txt` (Pillow, Faster-Whisper, SoundFile, NumPy).
3. Activate the unified `/video-editing` skill located in `00_CORE_SYSTEM/skills/video-editing/SKILL.md`.
4. Run the interactive 3-question Grill-Me protocol:
   - Ask me for the video topic/hook.
   - Ask me to choose a character archetype (Dev, Neha, Dr. Kabir, Arjun).
   - Ask me for the final Call-to-Action (CTA) and desired video save directory.
5. Once answered, autonomously write a pure Devanagari Hindi phonetic script, synthesize voiceover via the Multi-Provider Voice Vault, align word timestamps, and render a broadcast-grade 1080x1920 2D animated reel with zero-overflow subtitles.
```

---

## 3. Manual Step-by-Step Setup

### Step 1: Clone Repository
In your AI terminal:
```bash
git clone https://github.com/technicalknowledge8218/Master_Ai_Automation.git
cd Master_Ai_Automation
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Register API Keys in `.env`
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### Step 4: Register the Antigravity / Agent Skill
Copy the skill configuration into your local agent skills directory:
- **For Antigravity**:
  ```bash
  # Copy to user skills directory
  mkdir -p ~/.gemini/config/skills/video-editing
  cp 00_CORE_SYSTEM/skills/video-editing/SKILL.md ~/.gemini/config/skills/video-editing/SKILL.md
  ```
- **For Cursor / Claude**:
  Add `00_CORE_SYSTEM/skills/video-editing/SKILL.md` to your system rules or `.cursorrules`.

---

## 4. How to Create Videos with the Agent

Whenever you want to produce a video, simply type in your chat:
```text
/video-editing
```

The AI will immediately launch the **Grill-Me Protocol**:
1. **Topic**: What tech news, programming framework, or product are we covering?
2. **Character**: 
   - `Dev` (Tech Builder / Solo Explainer)
   - `Neha` (Host / Co-pilot)
   - `Dr. Kabir` (Senior Architect / Mentor)
   - `Arjun` (Young energetic creator)
3. **CTA & Destination**: Where to save (e.g. `Desktop/MyReels`) and what button/comment to request.

Once answered, the agent produces the entire video end-to-end without further interruption!
