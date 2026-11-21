# MASTER AI — STORYBOARD & CAMERA PLAN (PHASE 7.14)

**Document:** `storyboard_and_camera_plan.md`  
**Production:** *"The ₹10 Chai QR Code Scam"*  
**Target Medium:** Instagram Reels / YouTube Shorts (9:16 Vertical, 1080×1920)  
**Total Target Duration:** 32.0 Seconds (6 Motivated Shots)  
**Locked Visual Style:** `STYLE_VECTOR_EDITORIAL` (100% Vector Geometry, Zero Live-Action Mixing)  
**Cinematic Philosophy:** Every shot has a motivated camera angle, off-center compositional balance, and clear psychological intent.

---

## 1. CINEMATOGRAPHY & FRAMING PRINCIPLES (9:16 VERTICAL)

In vertical 9:16 video, conventional 16:9 cinematic conventions fail. We enforce the following spatial rules:

1. **Rule of Thirds & Diagonal Eyelines:** Protagonist and Antagonist never sit in the same horizontal axis. If Rohan is in the lower-right third looking up-left, Bunty must appear in the upper-left third looking down-right.
2. **Safe Action Margins:** All critical visual cues, facial expressions, and vector UI components are strictly bounded within `X: [120, 960]` and `Y: [240, 1680]`. The bottom 240px is reserved exclusively for centered, high-contrast captions and Instagram UI controls.
3. **Motivated Camera Dynamics:** No static camera holds beyond 2.0 seconds without an internal graphic zoom (`1.0x -> 1.08x`), simulated parallax drift, or animated vector UI transition.
4. **J-Cuts & Audio Continuity:** Sound effects and dialogue cues lead visual transitions by 150ms–250ms to create seamless, professional narrative flow.

---

## 2. SHOT-BY-SHOT STORYBOARD BLUEPRINT

```
+-----------------------------------------------------------------------------+
| SHOT 1: THE HOOK (0.0s - 2.0s)                                              |
| Framing: Extreme Macro Dutch Angle (5° tilt)                                |
| Action: Boiling cutting chai pouring from height; shiny fake QR sticker     |
|         peeling over rusted tin tea board.                                  |
| Audio: Sizzling hot tea sound + abrupt ominous synth drop.                  |
+-----------------------------------------------------------------------------+
                                     │
                                     ▼ (Match Cut on Glass Clink)
+-----------------------------------------------------------------------------+
| SHOT 2: THE DISCOVERY (2.0s - 7.5s)                                         |
| Framing: Medium Over-the-Shoulder (OTS), Rohan on Right Third               |
| Action: Rohan scans stall QR; phone UI flashes red alert: "Royal_999@fake". |
| Audio: UPI camera chime + Rohan internal dialogue: "Kalu bhaiya ka naam     |
|        'Royal Electronics' kab se ho gaya?"                                 |
+-----------------------------------------------------------------------------+
                                     │
                                     ▼ (Whip Pan Across Street)
+-----------------------------------------------------------------------------+
| SHOT 3: THE SUSPECT IN THE SHADOWS (7.5s - 13.0s)                           |
| Framing: Low-Angle Telephoto Medium Shot, Bunty on Left Third               |
| Action: Bunty in bomber jacket & sunglasses, casually checking smartwatch   |
|         alert for incoming ₹10 payments while pretending to sip tea.        |
| Audio: Subtle smartwatch notification ping + suspicious bass pulse.         |
+-----------------------------------------------------------------------------+
                                     │
                                     ▼ (Hard J-Cut into Action)
+-----------------------------------------------------------------------------+
| SHOT 4: THE COUNTER-TRAP & BLUFF (13.0s - 19.5s)                            |
| Framing: High-Impact Dynamic Split-Screen                                   |
| Action: Top: Innocent customer about to scan.                               |
|         Bottom: Rohan intercepts, taps phone: "Scanner mein live police     |
|         photo verification chal raha hai!"                                  |
| Camera: Rapid zoom punch on Bunty's face; vector sweat drops pop out.       |
+-----------------------------------------------------------------------------+
                                     │
                                     ▼ (Whip Pan to Stall Counter)
+-----------------------------------------------------------------------------+
| SHOT 5: THE CLIMAX / BRASS LADLE CHECKMATE (19.5s - 26.5s)                  |
| Framing: Wide Stall Profile with Dynamic Diagonal Lines                     |
| Action: Bunty lunges to snatch fake sticker. Kalu Bhaiya's long brass       |
|         tea ladle lands calmly on his shoulder from behind.                 |
| Audio: Resonant metallic ladle 'thud' + Kalu: "Subah se 3,000 rupaye        |
|         gaye hain tere account mein... pehle hisaab kar!"                   |
+-----------------------------------------------------------------------------+
                                     │
                                     ▼ (Smooth Dissolve)
+-----------------------------------------------------------------------------+
| SHOT 6: THE PUNCHLINE & CTA (26.5s - 32.0s)                                 |
| Framing: Clean Medium Close-Up, Rohan in center-right, Kalu smiling behind  |
| Action: Rohan raises hot chai glass to camera, delivers smart takeaway tip. |
| Graphics: Clean vector banner: "SCAN SE PEHLE NAAM PADHO!"                  |
| Audio: Warm Indian flute/lofi beat sting + upbeat closing cadence.          |
+-----------------------------------------------------------------------------+
```

---

## 3. DETAILED TECHNICAL SPECIFICATIONS PER SHOT

### SHOT 1: THE HOOK
- **Timecode:** `00:00.00` – `00:02.00` (2.0s)
- **Camera Focal Length:** Equivalent 85mm Macro.
- **Composition:** Asymmetric split focus. Foreground lower-left shows hot amber tea stream cascading into ribbed glass; background upper-right shows corner of tin QR stand with a corner-peeled glossy white sticker.
- **Color Temperature:** Warm amber (`#E67E22`) and deep charcoal (`#1E293B`).
- **Sound Design:**
  - `00:00.00`: Real foley tea boiling & pouring stream.
  - `00:01.20`: Sudden low sub-bass sweep (`80Hz -> 40Hz`).

### SHOT 2: THE DISCOVERY
- **Timecode:** `00:02.00` – `00:07.50` (5.5s)
- **Camera Focal Length:** Equivalent 35mm OTS.
- **Composition:** Rohan framed from torso up, standing in the right third of the 9:16 frame. His smartphone occupies the central vertical axis with an animated vector scan square (`#0284C7`) targeting the QR plate.
- **Animation Beat:** The scan resolves into a floating red warning dialog box (`#EF4444` border) showing *Payee: Royal_999@fakeupi | Merchant ID: Unverified*. Rohan's right eyebrow rises.
- **Voiceover:** Rohan (Edge-TTS `hi-IN-MadhurNeural`, natural cadence): *"Kalu bhaiya ki tapri pe roz chai peeta hoon... par aaj unka naam 'Royal Electronics' kab se ho gaya?"*

### SHOT 3: THE SUSPECT IN THE SHADOWS
- **Timecode:** `00:07.50` – `00:13.00` (5.5s)
- **Camera Focal Length:** Equivalent 50mm Low-Angle.
- **Composition:** Bunty staged on the left vertical third, partially obscured by the stall's cloth awning. Staging creates a voyeuristic angle.
- **Animation Beat:** Bunty lifts his wrist; vector smartwatch interface flashes a green "+₹10 Recd" message. A smirk curls on his lips, followed by a suspicious side-glance behind his sunglasses.
- **Voiceover (Internal):** *"Asli QR par nakli sticker chipka ke, subah se har customer ka paisa seedha apni jeb mein daal raha tha ye!"*

### SHOT 4: THE COUNTER-TRAP & BLUFF
- **Timecode:** `00:13.00` – `00:19.50` (6.5s)
- **Camera Dynamic:** Vertical split-screen transitioning to a rapid digital zoom-punch.
- **Composition:**
  - Top panel (40% height): Office employee extending phone to scan.
  - Bottom panel (60% height): Rohan stepping in front of the lens with a raised hand, winking directly at the viewer.
- **Action:** Rohan speaks loudly towards the crowd. Rapid 1.3x camera punch zooms into Bunty’s face. Two stylized vector sweat beads pop from his temple; his mouth drops in shock.
- **Dialogue:** Rohan: *"Arre Bhaiya ruko! Kalu bhaiya ne naya smart QR lagaya hai... jo bhi scan karega, scammer ka live photo seedha Cyber Cell police ko jayega!"*

### SHOT 5: THE CLIMAX / BRASS LADLE CHECKMATE
- **Timecode:** `00:19.50` – `00:26.50` (7.0s)
- **Camera Angle:** Dutch Angle 8° tilt, medium-wide.
- **Action Beat:**
  - `00:19.50`: Bunty scrambles forward in panic, fingers outstretched to rip off his fake sticker and destroy evidence.
  - `00:21.00`: A gleaming, long-handled brass ladle swings down smoothly from screen right, coming to rest firmly on Bunty’s bomber jacket shoulder.
  - `00:22.00`: Kalu Bhaiya steps into frame from behind the wooden counter, steam curling around his face, wearing a calm, knowing grin.
- **SFX:** Metallic brass impact 'clonk' (`#F59E0B` vector impact spark).
- **Dialogue:** Kalu Bhaiya (Edge-TTS `hi-IN-MadhurNeural`, deep pitch `-4Hz`): *"Subah se teen hazaar rupaye gaye hain tere account mein... pehle hisaab kar, fir bhaagna beta!"*

### SHOT 6: THE PUNCHLINE & TAKEAWAY
- **Timecode:** `00:26.50` – `00:32.00` (5.5s)
- **Camera Focal Length:** Equivalent 50mm Medium Close-Up.
- **Composition:** Rohan centered in the frame, lifting a steaming glass of cutting chai in a toast to the audience. In the background, Kalu Bhaiya is calmly holding Bunty by the collar while typing on his phone.
- **Graphic Elements:** Centered punchline banner sliding up from bottom safe margin:  
  `[ SCAN SE PEHLE DUKAAN KA NAAM CHECK KARO! ]` in bold white on emerald green banner (`#10B981`).
- **Dialogue / VO:** Rohan: *"Toh doston, UPI scan karte time dukaan ka naam zaroor verify karo... tech smart hai, tum bhi bano!"*
- **End Sting:** Upbeat melodic cadence with brand logo lockup.

---

## 4. AUDIO & SOUND DESIGN TIMELINE

```
0.0s          5.0s          10.0s         15.0s         20.0s         25.0s         32.0s
|-------------|-------------|-------------|-------------|-------------|-------------|
[TEA BOIL/POUR] 
              [UPI SCAN CHIME] 
                            [SUSPENSE BEAT] 
                                          [DRAMATIC PUNCH] 
                                                        [BRASS CLONK] 
                                                                      [UPBEAT FLUTE LOFI]
[ROGAN VO 1]----------------> [SUSPECT DISCOVERY]---------> [BLUFF DIALOGUE]---------> [KALU RECKONING]-----> [TAKEAWAY]--->
```

All audio tracks will be normalized to `-14.0 LUFS` with a maximum true peak of `-1.0 dBFS` to comply with Instagram/YouTube loudness standards.
