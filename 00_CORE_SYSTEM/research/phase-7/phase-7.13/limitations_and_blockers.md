# MASTER AI: LIMITATIONS, BOTTLENECKS & DEPENDENCY BLOCKERS
**Phase**: Phase 7.13 Real Capability Validation  
**Date**: 2026-11-18  
**Output Path**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.13\limitations_and_blockers.md`  

---

## 1. Concrete Hardware Blockers

1. **Integrated GPU (Intel Iris Xe) with Zero CUDA Acceleration**:
   - The workstation lacks a discrete NVIDIA GPU.
   - **Impact**: State-of-the-art open generative video diffusion models (Wan 2.1, LTX-Video, HunyuanVideo) cannot run locally. Attempting CPU inference takes hours per second or crashes with out-of-memory errors.
2. **C:\ Storage Exhaustion**:
   - `C:\` has only **10.86 GB free**.
   - **Impact**: Large PyTorch AI model checkpoints (typically 12 GB – 30 GB) cannot be downloaded or cached on the primary system drive. All production files must remain strictly pinned to `F:\Master AI` (325 GB free).

---

## 2. Software & Tooling Dependencies Missing / Not Installed

1. **OpenBone Engine Binary Missing**:
   - `openbone.exe`, `@openbone/mcp`, and the OpenBone player runtime do not exist on disk.
   - **Impact**: True skeletal bone rigging with free-form mesh deformation cannot be executed until the OpenBone binary or package is installed locally.
2. **Acoustic Phoneme Lip-Sync Engine Missing**:
   - No phoneme aligner (such as Rhubarb Lip Sync or Wav2Lip) is installed.
   - **Impact**: Lip movement is currently energy-driven viseme cycling rather than true phonetic mouth-shape matching.
3. **Pexels API Integration Not Hooked into 9:16 Vertical**:
   - `pexels_media_adapter.py` exists from Phase 6.5, but was authored for landscape wildlife clips. It requires an adapter update to search and crop vertical 9:16 urban and tech footage.

---

## 3. Creative Bottlenecks Identified in Test Film (Score: 5.8 / 10.0)

1. **2D Sprite vs. Fully Rigged Skeletal Mesh**:
   - While eliminating flat geometric SVG circles/rectangles, the character sprite still lacks smooth multi-joint skeletal inverse kinematics (IK) for walking and full body turns.
2. **Depth of Field & Lens Optics**:
   - The moving background video is sharp; adding real optical depth-of-field blur (Gaussian blur on background when camera focuses on character face) would significantly improve cinematic presentation.
3. **Typography Animation**:
   - Subtitles appear on high-contrast cards, but lack word-by-word active karaoke scaling.

---

## 4. Remediation Roadmap for Phase 7.14

| Identified Bottleneck | Proposed Engineering Solution | Zero-Cost Feasibility |
| :--- | :--- | :--- |
| **Skeletal 2D Rigging** | Clone OpenBone repository source or integrate Spine/Rive WebGL canvas renderer | High (Open-source MIT) |
| **Acoustic Lip-Sync** | Install Rhubarb Lip Sync CLI binary (open-source command-line tool) | High (Zero-cost, local CPU) |
| **Cinematic Depth of Field** | Add FFmpeg / OpenCV dynamic focal blur filter to background video | High (Immediate implementation) |
| **Kinetic Word Karaoke** | Generate ASS subtitle streams with `{\k<duration>}` timing tags | High (Immediate implementation) |
