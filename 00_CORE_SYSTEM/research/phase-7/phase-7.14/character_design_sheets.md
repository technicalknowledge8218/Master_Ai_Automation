# MASTER AI — CHARACTER DESIGN SHEETS (PHASE 7.14)

**Document:** `character_design_sheets.md`  
**Model Sheet Asset:** [character_model_sheet.png](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.14/character_model_sheet.png)  
**Production Format:** 9:16 Vertical Short Film  
**Visual Style Lock:** `STYLE_VECTOR_EDITORIAL` (Clean flat 2D vector forms, crisp linework, single-tier cel shading)  
**Strict Prohibition:** No photorealistic textures, no 3D live-action integration, no stock footage mixing.

---

## 1. VISUAL MODEL SHEET OVERVIEW

The character roster for **"The ₹10 Chai QR Code Scam"** consists of three carefully designed archetypes that mirror authentic Indian street-tech life while maintaining strict geometric cohesion with the 2D vector background environment.

![Character Model Sheet](file:///F:/Master%20AI/00_CORE_SYSTEM/research/phase-7/phase-7.14/character_model_sheet.png)

---

## 2. CHARACTER SPECIFICATIONS

### 1. ROHAN — THE PROTAGONIST
- **Archetype:** Observant College Student / Young Fintech Professional.
- **Age:** 22 years old.
- **Physical Build:** Lean athletic build, 7-head editorial proportion. Upright, confident posture.
- **Visual Features:**
  - Modern side-taper haircut with neat front fringe (`#0F172A`).
  - Warm Indian skin tone (`#E0A96D`) with subtle 20% alpha amber cel shadow (`#C89154`).
  - Expressive eyebrows: one arching slightly higher to convey analytical curiosity.
  - Casual street-smart attire: Deep navy open denim jacket (`#1E3A8A`) over mustard tee (`#F59E0B`), dark slate jeans (`#334155`), clean white sneakers (`#F8FAFC`).
  - Hero Accessory: Charcoal backpack single-strap worn diagonally; smartphone with bright blue vector screen glow.
- **Turnaround & Poses:**
  - *Front View:* Calm neutral stance, phone loosely held at waist.
  - *3/4 Action View:* Stepping forward, scanning QR code with phone angled at 45°.
  - *Close-Up:* Smirking sideways while tapping screen; one eyebrow raised in triumphant deduction.
- **Palette Hex Codes:**
  - Skin Base: `#E0A96D`
  - Skin Cel Shadow: `#C89154`
  - Denim Jacket: `#1E3A8A`
  - Inner T-Shirt: `#F59E0B`
  - Pants: `#334155`
  - UI Accent: `#0284C7`

---

### 2. BUNTY — THE ANTAGONIST / SCAMMER
- **Archetype:** Petty Digital Grifter / QR Sticker Swapper.
- **Age:** 25 years old.
- **Physical Build:** Slightly slouched posture, fidgety hands, 6.8-head proportion. Always angled sideways.
- **Visual Features:**
  - Messy spiky hair (`#1F2937`) with cheap oversized dark wrap-around sunglasses (`#0F172A` with cyan glare `#38BDF8`).
  - Wheatish complexion (`#D49B6A`).
  - Streetwear bomber jacket in charcoal grey (`#374151`) with crimson red zippers and accents (`#EF4444`).
  - Neon green Bluetooth neckband (`#10B981`) resting on collarbones.
  - Tapered black joggers (`#1E293B`) with red high-top sneakers (`#EF4444`).
  - Hero Props: Roll of adhesive fake QR stickers (`#FFFFFF` with black QR matrix) tucked into his palm; smartwatch showing payment alerts.
- **Turnaround & Poses:**
  - *Resting Pose:* Standing 4 paces away from tea stall, arms half-crossed, eyes darting behind sunglasses.
  - *Action Pose:* Swift leaning lunge to peel or stick fake decal.
  - *Reaction Pose:* Eyes widening with sweat beads popping off forehead, jaw dropping as a brass ladle taps his shoulder.
- **Palette Hex Codes:**
  - Skin Base: `#D49B6A`
  - Bomber Charcoal: `#374151`
  - Warning Red: `#EF4444`
  - Neon Accent: `#10B981`
  - Sunglasses: `#0F172A`
  - Sweat Drops: `#38BDF8`

---

### 3. KALU BHAIYA — THE MENTOR / TEA VENDOR
- **Archetype:** Street Tea Master & Respected Local Stall Owner.
- **Age:** 50 years old.
- **Physical Build:** Sturdy, broad-shouldered, grounded 6.5-head silhouette.
- **Visual Features:**
  - Receding graying temples (`#475569`) with a thick, iconic handlebar mustache (`#0F172A`).
  - Deep rich complexion (`#C68642`) with subtle laugh lines and crow's feet.
  - Traditional Indian street attire: Khadi cream cotton shirt (`#CBD5E1`) under a warm earth-brown waistcoat (`#B45309`), red-and-white checked *gamchha* cloth draped over the right shoulder (`#DC2626`).
  - Traditional brown leather slippers (`#78350F`).
  - Hero Prop: Long-handled antique polished brass tea ladle (`#F59E0B` / `#D97706`).
- **Turnaround & Poses:**
  - *Stall Stance:* Standing centered behind the tea stall counter, pouring cutting chai from 2 feet above the glass.
  - *Action Stance:* Extending the long brass ladle calmly across the frame to rest on Bunty's shoulder.
  - *Close-Up:* Knowing, calm, unhurried smile with sharp eyes that have seen every street trick.
- **Palette Hex Codes:**
  - Skin Base: `#C68642`
  - Cotton Khadi: `#CBD5E1`
  - Earth Vest: `#B45309`
  - Red Gamchha: `#DC2626`
  - Brass Ladle: `#F59E0B` / `#D97706`

---

## 3. TECHNICAL IMPLEMENTATION & ASSET REUSABILITY

1. **Vector Rigging Consistency:**  
   All characters share the exact same stroke width hierarchy:
   - Primary character silhouettes: `2.0px – 2.5px` solid dark slate stroke (`#0F172A`).
   - Internal apparel and feature details: `1.2px – 1.5px`.
   - Subtle cel shadows: `0px` stroke with flat fill at 25% opacity.

2. **Off-Center Vertical Framing Rules:**  
   - Characters are never positioned statically dead-center for consecutive shots.
   - Rohan occupies the right vertical third when scanning (looking left).
   - Bunty occupies the left vertical third in the background (looking right across).
   - This maintains proper visual eyelines and classic cinematic axis-of-action (*180-degree rule*).

3. **Lighting & Environment Harmonization:**  
   The tea stall counter, kettle steam, wooden benches, and street backdrop share the identical color harmony (warm morning sunlight `#FEF08A` coming from top-left, casting long slate shadows `#1E293B`).
