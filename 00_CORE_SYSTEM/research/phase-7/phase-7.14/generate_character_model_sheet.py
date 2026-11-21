"""
Master AI - Phase 7.14 Character Model Sheet Generator
Produces an editorial vector character model sheet for Concept B:
'The ₹10 Chai QR Code Scam' adhering strictly to STYLE_VECTOR_EDITORIAL.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
import os

def create_model_sheet():
    output_path = r'F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.14\character_model_sheet.png'
    
    # 16:9 widescreen presentation sheet: 2400 x 1350
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor('#0F172A') # Dark slate modern studio background
    ax.set_facecolor('#0F172A')
    
    # Grid limits 0 to 100 in both axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # --- HEADER SECTION ---
    # Top header bar
    header_box = patches.FancyBboxPatch((2, 91), 96, 7.5, boxstyle="round,pad=0.5", 
                                        fc="#1E293B", ec="#38BDF8", lw=1.5)
    ax.add_patch(header_box)
    
    ax.text(4, 95.5, "MASTER AI — PHASE 7.14 // CHARACTER MODEL SHEET", 
            fontsize=15, fontweight='bold', color='#38BDF8', family='sans-serif')
    ax.text(4, 92.5, "LOCKED STYLE: STYLE_VECTOR_EDITORIAL  |  PROJECT: THE ₹10 CHAI QR SCAM  |  FORMAT: 9:16 VERTICAL SHORT", 
            fontsize=9.5, fontweight='semibold', color='#94A3B8', family='sans-serif')
    ax.text(96, 94.0, "PALETTE: ZERO LIVE-ACTION MIX", 
            fontsize=10, fontweight='bold', color='#F59E0B', family='sans-serif', ha='right')

    # --- THREE CHARACTER SECTIONS ---
    
    # PANEL 1: ROHAN (PROTAGONIST) - Left 32%
    p1_box = patches.FancyBboxPatch((2, 4), 30, 85, boxstyle="round,pad=0.5", fc="#1E293B", ec="#334155", lw=1.2)
    ax.add_patch(p1_box)
    
    # Title & Role
    ax.text(4, 85.5, "ROHAN (PROTAGONIST)", fontsize=13, fontweight='bold', color='#38BDF8')
    ax.text(4, 83.2, "Role: Observant College Student (Age: 22)\nStyle: Crisp Clean Editorial Vector, 7-Head Proportion", 
            fontsize=8.5, color='#CBD5E1', linespacing=1.3)
    
    # Character Illustration: Rohan (Front & 3/4 Stance)
    # Background card inside panel
    char1_card = patches.FancyBboxPatch((4, 38), 26, 42, boxstyle="round,pad=0.3", fc="#0F172A", ec="#475569", lw=0.8)
    ax.add_patch(char1_card)
    
    # Vector Rohan Figure
    # Body / Jacket (Dark Navy Denim #1E3A8A)
    torso = patches.Polygon([[14, 46], [20, 46], [21, 56], [13, 56]], closed=True, fc='#1E3A8A', ec='#0F172A', lw=2)
    ax.add_patch(torso)
    # Inner T-Shirt (Mustard Gold #F59E0B)
    tshirt = patches.Polygon([[15.5, 52], [18.5, 52], [18, 56], [16, 56]], closed=True, fc='#F59E0B', ec='#0F172A', lw=1.5)
    ax.add_patch(tshirt)
    # Backpack Strap (Diagonal #334155)
    strap = patches.Polygon([[14.5, 56], [16, 56], [20.5, 46], [19.2, 46]], closed=True, fc='#334155', ec='#0F172A', lw=1.2)
    ax.add_patch(strap)
    # Neck (#FBCFE8 / Indian Warm Skin #E0A96D)
    neck = patches.Rectangle((16, 55.5), 2, 2.5, fc='#E0A96D', ec='#0F172A', lw=1.5)
    ax.add_patch(neck)
    # Head (#E0A96D)
    head = patches.Circle((17, 60.5), 3.2, fc='#E0A96D', ec='#0F172A', lw=2)
    ax.add_patch(head)
    # Cel Shadow on Face
    shadow = patches.Wedge((17, 60.5), 3.2, 270, 90, fc='#C89154', alpha=0.35)
    ax.add_patch(shadow)
    # Modern Hair Cut (#1E293B, slick fade)
    hair = patches.Polygon([[13.8, 61], [15, 64.2], [18.5, 64.2], [20.2, 61.5], [19.5, 60], [17, 62], [14.5, 60]], 
                           closed=True, fc='#0F172A', ec='#0F172A', lw=1.5)
    ax.add_patch(hair)
    # Eyes & Eyebrow (Sharp, analytical)
    ax.plot([15.2, 16.5], [60.8, 60.8], color='#0F172A', lw=2) # left brow
    ax.plot([17.5, 18.8], [61.1, 60.6], color='#0F172A', lw=2) # right brow raised
    ax.plot([15.8], [60.1], marker='o', color='#0F172A', markersize=3)
    ax.plot([18.2], [60.1], marker='o', color='#0F172A', markersize=3)
    # Confident Smirk
    ax.plot([16.5, 18.0], [58.8, 59.1], color='#0F172A', lw=1.8)
    
    # Legs (Slim Jeans #334155)
    leg_l = patches.Polygon([[14, 39], [16.5, 39], [16.8, 46], [14.2, 46]], closed=True, fc='#334155', ec='#0F172A', lw=1.5)
    leg_r = patches.Polygon([[17.5, 39], [20, 39], [19.8, 46], [17.2, 46]], closed=True, fc='#334155', ec='#0F172A', lw=1.5)
    ax.add_patch(leg_l)
    ax.add_patch(leg_r)
    # Sneakers (#F8FAFC white)
    ax.add_patch(patches.Rectangle((13.5, 38.2), 3, 1.2, fc='#F8FAFC', ec='#0F172A', lw=1.2))
    ax.add_patch(patches.Rectangle((17.5, 38.2), 3, 1.2, fc='#F8FAFC', ec='#0F172A', lw=1.2))
    
    # Phone in Hand (Vector UI Glow)
    phone = patches.Rectangle((20.5, 48), 2.5, 4.5, angle=-10, fc='#0284C7', ec='#F8FAFC', lw=1.2)
    ax.add_patch(phone)
    
    # Color Palette Swatches for Rohan
    ax.text(4, 35, "COLOR DNA & PALETTE", fontsize=9, fontweight='bold', color='#94A3B8')
    swatches_rohan = [
        ('#E0A96D', 'Skin Warm'),
        ('#1E3A8A', 'Jacket Navy'),
        ('#F59E0B', 'Mustard Tee'),
        ('#334155', 'Denim Dark'),
        ('#0284C7', 'Fintech Cyan')
    ]
    for i, (col, lbl) in enumerate(swatches_rohan):
        ax.add_patch(patches.Rectangle((4 + i*5.2, 29), 4.5, 4.5, fc=col, ec='#0F172A', lw=1))
        ax.text(4 + i*5.2 + 2.25, 27.2, lbl, fontsize=6.2, ha='center', color='#94A3B8')
        ax.text(4 + i*5.2 + 2.25, 25.5, col, fontsize=6, ha='center', color='#64748B')
        
    # Expressions Box
    ax.text(4, 22.5, "KEY EXPRESSIONS:", fontsize=8.5, fontweight='bold', color='#CBD5E1')
    ax.text(4, 18.5, "1. The Curious Squint (noticing fake sticker)\n2. The Analytical Smirk (crafting counter-bluff)\n3. The Direct Camera Punchline (empowered tip)",
            fontsize=7.8, color='#94A3B8', linespacing=1.3)
    ax.text(4, 12, "STROKE: 2.0px Solid Slate (#0F172A)\nSHADING: Single-tier 20% flat cel shadow\nFORBIDDEN: Gradients, realism, stock textures",
            fontsize=7.5, color='#F87171', fontweight='semibold')

    # PANEL 2: BUNTY (THE SCAMMER) - Middle 32%
    p2_box = patches.FancyBboxPatch((35, 4), 30, 85, boxstyle="round,pad=0.5", fc="#1E293B", ec="#334155", lw=1.2)
    ax.add_patch(p2_box)
    
    ax.text(37, 85.5, "BUNTY (THE SCAMMER)", fontsize=13, fontweight='bold', color='#F59E0B')
    ax.text(37, 83.2, "Role: Petty Tech Grifter / QR Sticker Swapper (Age: 25)\nStyle: Shifty body language, high-contrast neon accents", 
            fontsize=8.5, color='#CBD5E1')
            
    # Character Illustration: Bunty
    char2_card = patches.FancyBboxPatch((37, 38), 26, 42, boxstyle="round,pad=0.3", fc="#0F172A", ec="#475569", lw=0.8)
    ax.add_patch(char2_card)
    
    # Vector Bunty Figure (Slouched, suspicious stance)
    # Bomber Jacket (#DC2626 Crimson / Charcoal #374151)
    torso_b = patches.Polygon([[47, 46], [53, 46], [54.5, 55.5], [45.5, 55.5]], closed=True, fc='#374151', ec='#0F172A', lw=2)
    ax.add_patch(torso_b)
    # Crimson Zippers & Collar
    ax.plot([47, 49.5, 50.5, 53], [55.5, 53, 53, 55.5], color='#EF4444', lw=2.5)
    # Neckband headphones (#10B981 Neon green tips)
    ax.plot([47.5, 49, 51, 52.5], [56, 53.5, 53.5, 56], color='#10B981', lw=2)
    # Neck & Head (#D49B6A)
    ax.add_patch(patches.Rectangle((49, 55), 2, 2.5, fc='#D49B6A', ec='#0F172A', lw=1.5))
    head_b = patches.Circle((50, 60), 3.1, fc='#D49B6A', ec='#0F172A', lw=2)
    ax.add_patch(head_b)
    # Spiky Messy Hair (#1F2937)
    hair_b = patches.Polygon([[47, 60.5], [47.5, 63.8], [49, 62.5], [51, 64.5], [53, 62], [53.5, 60]], 
                             closed=True, fc='#0F172A', ec='#0F172A', lw=1.5)
    ax.add_patch(hair_b)
    # Dark Wrap Sunglasses (#0F172A with neon reflection)
    ax.add_patch(patches.Rectangle((47.8, 59.5), 4.4, 1.8, fc='#0F172A', ec='#1E293B', lw=1.2))
    ax.plot([48.5, 51.5], [60.6, 60.6], color='#38BDF8', lw=1) # glare highlight
    # Panicked sweat beads (cel vector teardrop)
    ax.add_patch(patches.Circle((53.8, 61), 0.6, fc='#38BDF8', ec='#0F172A', lw=0.8))
    ax.add_patch(patches.Circle((54.5, 59.5), 0.4, fc='#38BDF8', ec='#0F172A', lw=0.8))
    # Nervous mouth (wavy line)
    ax.plot([48.8, 49.5, 50.2, 51.0], [57.8, 58.2, 57.7, 58.0], color='#0F172A', lw=1.8)
    
    # Tapered Joggers (#1E293B) & Fake High-tops
    leg_bl = patches.Polygon([[47, 39], [49.5, 39], [49.8, 46], [47.2, 46]], closed=True, fc='#1E293B', ec='#0F172A', lw=1.5)
    leg_br = patches.Polygon([[50.5, 39], [53, 39], [52.8, 46], [50.2, 46]], closed=True, fc='#1E293B', ec='#0F172A', lw=1.5)
    ax.add_patch(leg_bl)
    ax.add_patch(leg_br)
    ax.add_patch(patches.Rectangle((46.5, 38.2), 3.2, 1.2, fc='#EF4444', ec='#0F172A', lw=1.2))
    ax.add_patch(patches.Rectangle((50.5, 38.2), 3.2, 1.2, fc='#EF4444', ec='#0F172A', lw=1.2))
    
    # Fake QR Sticker Roll in hand
    ax.add_patch(patches.Circle((44.5, 48), 1.6, fc='#FFFFFF', ec='#0F172A', lw=1.5))
    ax.add_patch(patches.Rectangle((43.7, 47.2), 1.6, 1.6, fc='#0F172A')) # mini QR motif
    
    # Palette Bunty
    ax.text(37, 35, "COLOR DNA & PALETTE", fontsize=9, fontweight='bold', color='#94A3B8')
    swatches_bunty = [
        ('#D49B6A', 'Skin Tone'),
        ('#374151', 'Bomber Charcoal'),
        ('#EF4444', 'Alert Crimson'),
        ('#10B981', 'Neckband Green'),
        ('#FFFFFF', 'Fake QR White')
    ]
    for i, (col, lbl) in enumerate(swatches_bunty):
        ax.add_patch(patches.Rectangle((37 + i*5.2, 29), 4.5, 4.5, fc=col, ec='#0F172A', lw=1))
        ax.text(37 + i*5.2 + 2.25, 27.2, lbl, fontsize=6.2, ha='center', color='#94A3B8')
        ax.text(37 + i*5.2 + 2.25, 25.5, col, fontsize=6, ha='center', color='#64748B')
        
    ax.text(37, 22.5, "KEY EXPRESSIONS:", fontsize=8.5, fontweight='bold', color='#CBD5E1')
    ax.text(37, 18.5, "1. Shifty Glancing Side-eye (checking for police/chime)\n2. Fake Innocent Smile (trying to blend in)\n3. Full Panic Jaw-Drop (caught red-handed by ladle)",
            fontsize=7.8, color='#94A3B8', linespacing=1.3)
    ax.text(37, 12, "BODY LANGUAGE: Slouched shoulders, rapid head turns\nACCESSORIES: Bluetooth neckband, smart watch, QR sheets\nPROP: Peeling adhesive QR sticker",
            fontsize=7.5, color='#FBBF24', fontweight='semibold')

    # PANEL 3: KALU BHAIYA (THE CHAIWALA) - Right 32%
    p3_box = patches.FancyBboxPatch((68, 4), 30, 85, boxstyle="round,pad=0.5", fc="#1E293B", ec="#334155", lw=1.2)
    ax.add_patch(p3_box)
    
    ax.text(70, 85.5, "KALU BHAIYA (CHAIWALA)", fontsize=13, fontweight='bold', color='#10B981')
    ax.text(70, 83.2, "Role: Street Tea Master & Respected Veteran (Age: 50)\nStyle: Grounded, sturdy silhouette, warm authority", 
            fontsize=8.5, color='#CBD5E1')
            
    # Character Illustration: Kalu Bhaiya
    char3_card = patches.FancyBboxPatch((70, 38), 26, 42, boxstyle="round,pad=0.3", fc="#0F172A", ec="#475569", lw=0.8)
    ax.add_patch(char3_card)
    
    # Vector Kalu Figure
    # Kurta / Shirt (#E2E8F0 Off-white) & Waistcoat (#B45309 Warm Brown)
    torso_k = patches.Polygon([[80, 45], [88, 45], [89, 55], [79, 55]], closed=True, fc='#B45309', ec='#0F172A', lw=2)
    ax.add_patch(torso_k)
    # Gamchha / Cloth on shoulder (#DC2626 Red check pattern)
    gamchha = patches.Polygon([[79, 55], [82, 55], [81, 46], [78.5, 46]], closed=True, fc='#DC2626', ec='#0F172A', lw=1.5)
    ax.add_patch(gamchha)
    # Neck & Head (#C68642 Deep Indian Complexion)
    ax.add_patch(patches.Rectangle((83, 54.5), 2.5, 2.5, fc='#C68642', ec='#0F172A', lw=1.5))
    head_k = patches.Circle((84.2, 59.5), 3.4, fc='#C68642', ec='#0F172A', lw=2)
    ax.add_patch(head_k)
    # Receding Hair with gray sideburns
    hair_k = patches.Polygon([[81, 60], [82, 63], [86.5, 63], [87.5, 60], [87, 58], [85, 61], [81.5, 58]], 
                             closed=True, fc='#475569', ec='#0F172A', lw=1.5)
    ax.add_patch(hair_k)
    # Prominent Indian Mustache (#1E293B)
    ax.plot([81.8, 83.5, 84.2, 85.0, 86.8], [58.2, 58.7, 58.4, 58.7, 58.2], color='#0F172A', lw=3.2)
    # Calm, Wise Eyes & Laugh Lines
    ax.plot([82.5, 83.6], [60.0, 60.0], color='#0F172A', lw=2)
    ax.plot([84.8, 85.9], [60.0, 60.0], color='#0F172A', lw=2)
    ax.plot([82.0, 82.3], [59.6, 59.9], color='#0F172A', lw=1) # crow's feet
    ax.plot([86.4, 86.1], [59.6, 59.9], color='#0F172A', lw=1)
    
    # Traditional Cotton Trousers (#CBD5E1)
    leg_kl = patches.Polygon([[80, 39], [83.5, 39], [83.8, 45], [80.2, 45]], closed=True, fc='#CBD5E1', ec='#0F172A', lw=1.5)
    leg_kr = patches.Polygon([[84.5, 39], [88, 39], [87.8, 45], [84.2, 45]], closed=True, fc='#CBD5E1', ec='#0F172A', lw=1.5)
    ax.add_patch(leg_kl)
    ax.add_patch(leg_kr)
    # Traditional Kolhapuri/Leather Slippers (#78350F)
    ax.add_patch(patches.Rectangle((79.5, 38.2), 4, 1.2, fc='#78350F', ec='#0F172A', lw=1.2))
    ax.add_patch(patches.Rectangle((84.5, 38.2), 4, 1.2, fc='#78350F', ec='#0F172A', lw=1.2))
    
    # Hero Prop: Brass Chai Ladle (Long handle reaching down)
    ax.plot([88, 89.5, 93], [52, 48, 42], color='#D97706', lw=3) # brass handle
    ax.add_patch(patches.Circle((93.5, 41.5), 1.8, fc='#F59E0B', ec='#0F172A', lw=1.5)) # brass cup
    
    # Palette Kalu
    ax.text(70, 35, "COLOR DNA & PALETTE", fontsize=9, fontweight='bold', color='#94A3B8')
    swatches_kalu = [
        ('#C68642', 'Skin Deep'),
        ('#B45309', 'Vest Brown'),
        ('#DC2626', 'Gamchha Red'),
        ('#F59E0B', 'Brass Gold'),
        ('#CBD5E1', 'Cotton Khadi')
    ]
    for i, (col, lbl) in enumerate(swatches_kalu):
        ax.add_patch(patches.Rectangle((70 + i*5.2, 29), 4.5, 4.5, fc=col, ec='#0F172A', lw=1))
        ax.text(70 + i*5.2 + 2.25, 27.2, lbl, fontsize=6.2, ha='center', color='#94A3B8')
        ax.text(70 + i*5.2 + 2.25, 25.5, col, fontsize=6, ha='center', color='#64748B')
        
    ax.text(70, 22.5, "KEY EXPRESSIONS:", fontsize=8.5, fontweight='bold', color='#CBD5E1')
    ax.text(70, 18.5, "1. The Pouring Focus (high stream tea mastery)\n2. Warm Welcoming Grin (regular customers)\n3. Stern Heavy-Ladle Reckoning (demanding stolen money)",
            fontsize=7.8, color='#94A3B8', linespacing=1.3)
    ax.text(70, 12, "HERO PROP: Long-handled antique brass tea ladle\nSTAGING: Always positioned behind stall counter or framing\nVOICE: Deep, resonant, calm unhurried Hindi",
            fontsize=7.5, color='#34D399', fontweight='semibold')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Character Model Sheet rendered successfully to: {output_path}")

if __name__ == '__main__':
    create_model_sheet()
