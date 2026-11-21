"""
Master AI - Phase 7.14 Sample Frame Renderer
Generates 6 production-grade sample frames (1080x1920 9:16 vertical)
for each scene of 'The ₹10 Chai QR Code Scam' adhering strictly to STYLE_VECTOR_EDITORIAL.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.14\sample_frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_canvas():
    # 9:16 Vertical canvas: 1080 x 1920 (at dpi=120, figsize=(9, 16))
    fig, ax = plt.subplots(figsize=(9, 16), dpi=120)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 192)
    ax.axis('off')
    return fig, ax

def add_safe_zone_overlays(ax, scene_num, scene_title, timecode):
    # Top info header card
    info_box = patches.FancyBboxPatch((6, 178), 96, 9, boxstyle="round,pad=0.6",
                                      fc="#1E293B", ec="#38BDF8", lw=1.2, alpha=0.92)
    ax.add_patch(info_box)
    ax.text(10, 182.5, f"SCENE 0{scene_num}: {scene_title.upper()}", 
            fontsize=11.5, fontweight='bold', color='#38BDF8', family='sans-serif')
    ax.text(10, 179.5, f"MASTER AI // PHASE 7.14  |  TIMECODE: {timecode}  |  STYLE_VECTOR_EDITORIAL", 
            fontsize=8.5, fontweight='semibold', color='#94A3B8', family='sans-serif')
    
    # Bottom safe margin banner for captions
    sub_box = patches.FancyBboxPatch((8, 12), 92, 11, boxstyle="round,pad=0.5",
                                     fc="#0F172A", ec="#475569", lw=1.2, alpha=0.95)
    ax.add_patch(sub_box)

def render_scene_1():
    # SCENE 1: THE HOOK (Macro Dutch Angle: Boiling tea stream & peeling fake sticker)
    fig, ax = setup_canvas()
    
    # Background: Warm street tea stall counter (#1E1B18)
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#1A1510'))
    
    # Wooden stall counter with grain geometry
    ax.add_patch(patches.Polygon([[0, 0], [108, 0], [108, 70], [0, 85]], closed=True, fc='#451A03', ec='#270F03', lw=2))
    ax.plot([0, 108], [75, 60], color='#270F03', lw=2)
    
    # Rusted Tin Sheet Background (#78350F)
    ax.add_patch(patches.Polygon([[10, 90], [98, 80], [98, 168], [10, 172]], closed=True, fc='#332219', ec='#1A110B', lw=2))
    
    # Rusted Metal QR Plate attached to wood
    qr_stand = patches.Polygon([[52, 95], [92, 90], [90, 150], [50, 155]], closed=True, fc='#D1D5DB', ec='#1F2937', lw=3)
    ax.add_patch(qr_stand)
    ax.text(71, 145, "KALU CHAIWALA", fontsize=9, fontweight='bold', color='#111827', ha='center', rotation=-4)
    # Original QR code matrix lines
    ax.add_patch(patches.Rectangle((56, 102), 30, 35, fc='#FFFFFF', ec='#111827', lw=1.5, angle=-4))
    
    # FAKE QR STICKER (White glossy decal peeling at corner!)
    fake_sticker = patches.Polygon([[59, 106], [87, 103], [85, 136], [62, 138]], closed=True, fc='#FFFFFF', ec='#EF4444', lw=2)
    ax.add_patch(fake_sticker)
    # Peeling Dog-Ear Corner (lifted off with shadow)
    ax.add_patch(patches.Polygon([[59, 106], [64, 114], [57, 112]], closed=True, fc='#E2E8F0', ec='#94A3B8', lw=1.2))
    ax.add_patch(patches.Polygon([[56, 104], [59, 106], [57, 112]], closed=True, fc='#000000', alpha=0.35))
    ax.text(73, 120, "[ FAKE QR ]\nRoyal_999", fontsize=8, fontweight='bold', color='#DC2626', ha='center', rotation=-4)
    
    # Suspicious Hand (Vector) entering from top-left peeling sticker
    hand = patches.Polygon([[20, 135], [45, 122], [58, 112], [56, 106], [42, 115], [15, 122]], closed=True, fc='#D49B6A', ec='#0F172A', lw=2)
    ax.add_patch(hand)
    
    # FOREGROUND MACRO: Cutting Chai Glass & Boiling Stream (Dutch Angle)
    # Ribbed Cutting Glass (#93C5FD transparent vector)
    glass = patches.Polygon([[18, 25], [42, 22], [39, 78], [15, 82]], closed=True, fc='#60A5FA', ec='#1E3A8A', lw=2.5, alpha=0.55)
    ax.add_patch(glass)
    # Hot Golden Chai inside glass
    chai_liquid = patches.Polygon([[19, 27], [41, 24], [38, 62], [16, 65]], closed=True, fc='#D97706', ec='#B45309', lw=1.5)
    ax.add_patch(chai_liquid)
    
    # Steaming High Pour Stream cascading from top
    stream = patches.Polygon([[26, 64], [30, 64], [33, 170], [30, 170]], closed=True, fc='#F59E0B', ec='#B45309', lw=1.5)
    ax.add_patch(stream)
    # Steam curls (vector ripples)
    for y_s in [70, 95, 120, 145]:
        ax.plot([24, 30, 36], [y_s, y_s+8, y_s+14], color='#FEF3C7', lw=2.5, alpha=0.6)
        
    # Dramatic Attention Indicator Arrow
    ax.annotate("FAKE STICKER\nPEELED OVER ORIGINAL!", xy=(60, 110), xytext=(22, 92),
                arrowprops=dict(facecolor='#EF4444', shrink=0.08, width=2.5, headwidth=8),
                fontsize=8.5, fontweight='bold', color='#EF4444', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#FEF2F2", ec="#EF4444", lw=1.5))
                
    add_safe_zone_overlays(ax, 1, "The Hook (Macro Dutch Angle)", "00:00.00 - 00:02.00")
    ax.text(54, 17.5, "SFX: Sizzling boiling chai + ominous sub-bass drop", fontsize=9.5, fontweight='bold', color='#F59E0B', ha='center')
    ax.text(54, 14.0, "[Visual Hook: High chai pour cuts to suspicious peeling QR sticker]", fontsize=8.5, color='#94A3B8', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_01_macro_hook.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 1 rendered:", save_path)

def render_scene_2():
    # SCENE 2: THE DISCOVERY (Rohan OTS right-third scanning, vector UI red warning alert)
    fig, ax = setup_canvas()
    
    # Background: Tea stall atmosphere (#1E293B)
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#0F172A'))
    # Stall shelf with kettle and chai glasses
    ax.add_patch(patches.Rectangle((0, 80), 55, 30, fc='#334155', ec='#1E293B', lw=1.5))
    # Brass kettle silhouette
    ax.add_patch(patches.Circle((20, 95), 10, fc='#D97706', ec='#78350F', lw=2))
    ax.add_patch(patches.Rectangle((18, 105), 4, 6, fc='#78350F'))
    
    # Stall QR stand on counter
    ax.add_patch(patches.Rectangle((35, 88), 18, 22, fc='#E2E8F0', ec='#0F172A', lw=2))
    ax.add_patch(patches.Rectangle((38, 92), 12, 14, fc='#0F172A'))
    
    # ROHAN (Framed on Right Third in 9:16 vertical OTS stance)
    # Torso (Denim Jacket #1E3A8A)
    torso = patches.Polygon([[62, 28], [108, 28], [108, 115], [58, 115]], closed=True, fc='#1E3A8A', ec='#0F172A', lw=3)
    ax.add_patch(torso)
    # Mustard Tee Collar
    ax.add_patch(patches.Polygon([[70, 115], [82, 115], [78, 104], [72, 104]], closed=True, fc='#F59E0B', ec='#0F172A', lw=1.8))
    # Diagonal Backpack Strap
    ax.add_patch(patches.Polygon([[64, 115], [70, 115], [105, 35], [98, 35]], closed=True, fc='#334155', ec='#0F172A', lw=2))
    # Head & Neck in Profile / 3-Quarter
    ax.add_patch(patches.Rectangle((72, 114), 8, 8, fc='#E0A96D', ec='#0F172A', lw=2))
    ax.add_patch(patches.Circle((76, 130), 11, fc='#E0A96D', ec='#0F172A', lw=2.5))
    # Cel Shadow
    ax.add_patch(patches.Wedge((76, 130), 11, 270, 90, fc='#C89154', alpha=0.35))
    # Modern Fade Hair
    ax.add_patch(patches.Polygon([[66, 132], [70, 143], [84, 143], [88, 135], [86, 126], [78, 134], [67, 126]],
                                 closed=True, fc='#0F172A', ec='#0F172A', lw=2))
    # Analytical Eyebrow & Squint
    ax.plot([70, 75], [131, 133], color='#0F172A', lw=2.5) # raised brow
    ax.plot([71], [129], marker='o', color='#0F172A', markersize=4) # eye looking at phone
    
    # Hand holding phone extending into center frame
    ax.add_patch(patches.Polygon([[54, 75], [68, 70], [66, 85], [52, 90]], closed=True, fc='#E0A96D', ec='#0F172A', lw=2))
    
    # SMARTPHONE INTERFACE (Vector UI Overlay - Center Frame)
    phone_body = patches.FancyBboxPatch((22, 60), 38, 72, boxstyle="round,pad=1.2",
                                        fc='#020617', ec='#38BDF8', lw=2.5)
    ax.add_patch(phone_body)
    
    # Phone Screen Content
    ax.add_patch(patches.Rectangle((24, 63), 34, 66, fc='#0F172A'))
    # Camera Viewfinder Scanner Box
    ax.add_patch(patches.Rectangle((28, 88), 26, 26, fc='none', ec='#38BDF8', lw=2, ls='--'))
    ax.text(41, 117, "UPI SCANNER ACTIVE", fontsize=7.5, fontweight='bold', color='#38BDF8', ha='center')
    
    # ALERT DIALOG CARD (Vector UI Popup)
    alert_card = patches.FancyBboxPatch((25, 68), 32, 24, boxstyle="round,pad=0.5",
                                        fc='#FEF2F2', ec='#EF4444', lw=2)
    ax.add_patch(alert_card)
    ax.text(41, 87, "⚠️ PAYEE MISMATCH!", fontsize=8.5, fontweight='bold', color='#DC2626', ha='center')
    ax.text(41, 80, "Pay To: Royal_999@fake\nExpected: Kalu_Chai@bank", fontsize=7.2, color='#1F2937', ha='center', linespacing=1.2)
    ax.text(41, 71.5, "Amount: ₹10.00", fontsize=7.5, fontweight='bold', color='#16A34A', ha='center')
    
    add_safe_zone_overlays(ax, 2, "The Discovery (OTS View)", "00:02.00 - 00:07.50")
    ax.text(54, 18.0, "ROHAN: 'Kalu bhaiya ki tapri pe roz chai peeta hoon...'", fontsize=9.5, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(54, 14.5, "par aaj unka naam 'Royal Electronics' kab se ho gaya?", fontsize=9.2, color='#FBBF24', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_02_rohan_scan.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 2 rendered:", save_path)

def render_scene_3():
    # SCENE 3: THE SUSPECT (Bunty in shadows on left third, checking smartwatch alert)
    fig, ax = setup_canvas()
    
    # Background: Alley corner / tea stall cloth awning (#1E293B)
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#0F172A'))
    # Red-white striped cloth awning above
    for i in range(8):
        c = '#DC2626' if i%2 == 0 else '#F8FAFC'
        ax.add_patch(patches.Polygon([[i*14, 192], [(i+1)*14, 192], [(i+1)*14, 150], [i*14, 155]], closed=True, fc=c, ec='#0F172A', lw=1.2))
        
    # Stall wooden pillar on right edge
    ax.add_patch(patches.Rectangle((88, 25), 14, 150, fc='#78350F', ec='#451A03', lw=2))
    
    # BUNTY (Framed in Left Third - Suspicious Slouched Stance)
    # Charcoal Bomber Jacket with Red Zipper
    torso = patches.Polygon([[18, 45], [44, 45], [48, 110], [14, 110]], closed=True, fc='#374151', ec='#0F172A', lw=3)
    ax.add_patch(torso)
    # Red Zippers
    ax.plot([18, 30, 32, 44], [110, 95, 95, 110], color='#EF4444', lw=2.5)
    # Neon Green Neckband
    ax.plot([20, 27, 35, 42], [112, 98, 98, 112], color='#10B981', lw=2.5)
    
    # Neck & Head
    ax.add_patch(patches.Rectangle((27, 108), 8, 8, fc='#D49B6A', ec='#0F172A', lw=2))
    ax.add_patch(patches.Circle((31, 126), 11, fc='#D49B6A', ec='#0F172A', lw=2.5))
    # Spiky Messy Hair
    ax.add_patch(patches.Polygon([[20, 127], [22, 140], [29, 134], [35, 142], [42, 133], [44, 126]],
                                 closed=True, fc='#1F2937', ec='#0F172A', lw=2))
    # Dark Wrap Sunglasses with cyan reflection
    ax.add_patch(patches.Rectangle((23, 122), 17, 7, fc='#0F172A', ec='#334155', lw=1.5))
    ax.plot([26, 37], [126, 126], color='#38BDF8', lw=1.5)
    # Shifty smirk
    ax.plot([26, 30, 35], [115, 114, 116], color='#0F172A', lw=2)
    
    # Arm raised looking at Smartwatch
    ax.add_patch(patches.Polygon([[38, 90], [55, 82], [60, 95], [42, 102]], closed=True, fc='#374151', ec='#0F172A', lw=2))
    ax.add_patch(patches.Rectangle((58, 85), 6, 8, fc='#D49B6A', ec='#0F172A', lw=1.5))
    
    # SMARTWATCH POPUP CALLOUT (Vector UI Graphic)
    watch_card = patches.FancyBboxPatch((58, 100), 44, 40, boxstyle="round,pad=1.0",
                                        fc='#020617', ec='#10B981', lw=2.5)
    ax.add_patch(watch_card)
    ax.plot([58, 54], [105, 93], color='#10B981', lw=2) # connector line to watch
    
    ax.text(80, 132, "SMARTWATCH ALERT", fontsize=8, fontweight='bold', color='#10B981', ha='center')
    ax.add_patch(patches.FancyBboxPatch((62, 105), 36, 22, boxstyle="round,pad=0.3", fc='#1E293B', ec='#334155'))
    ax.text(80, 120, "🔔 + ₹10.00 RECD!", fontsize=9.5, fontweight='bold', color='#4ADE80', ha='center')
    ax.text(80, 113, "From: Tapri_Customer_04", fontsize=7.2, color='#94A3B8', ha='center')
    ax.text(80, 107, "Total Scam Today: ₹3,140", fontsize=7.2, fontweight='bold', color='#F59E0B', ha='center')
    
    # Fake sticker roll visible tucked in his jacket pocket
    ax.add_patch(patches.Circle((20, 75), 4, fc='#FFFFFF', ec='#0F172A', lw=1.8))
    ax.text(20, 75, "QR", fontsize=5.5, fontweight='bold', color='#0F172A', ha='center', va='center')
    
    add_safe_zone_overlays(ax, 3, "The Suspect in Shadows", "00:07.50 - 00:13.00")
    ax.text(54, 18.0, "ROHAN (VO): 'Asli QR par nakli sticker chipka ke...'", fontsize=9.5, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(54, 14.5, "poore din ka dhandha apni jeb mein daal raha tha ye banda!", fontsize=9.2, color='#F87171', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_03_bunty_shadows.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 3 rendered:", save_path)

def render_scene_4():
    # SCENE 4: THE COUNTER-TRAP (Split screen / Intercept + Panicked Bunty)
    fig, ax = setup_canvas()
    
    # Background Split
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#0F172A'))
    
    # TOP PANEL (Y: 100 to 175): Office guy about to scan vs Rohan stepping in
    top_panel = patches.Rectangle((4, 100), 100, 74, fc='#1E293B', ec='#475569', lw=2)
    ax.add_patch(top_panel)
    ax.text(8, 168, "THE INTERVENTION", fontsize=9, fontweight='bold', color='#38BDF8')
    
    # Office Guy (Left of top panel)
    ax.add_patch(patches.Circle((25, 145), 7, fc='#E0A96D', ec='#0F172A', lw=1.8))
    ax.add_patch(patches.Polygon([[16, 102], [34, 102], [32, 138], [18, 138]], closed=True, fc='#0284C7', ec='#0F172A', lw=2))
    # Office guy holding phone
    ax.add_patch(patches.Rectangle((32, 125), 8, 14, fc='#020617', ec='#F8FAFC', lw=1.2))
    
    # Rohan stepping in between (Right of top panel)
    ax.add_patch(patches.Circle((68, 146), 7, fc='#E0A96D', ec='#0F172A', lw=1.8))
    ax.add_patch(patches.Polygon([[58, 102], [78, 102], [76, 139], [60, 139]], closed=True, fc='#1E3A8A', ec='#0F172A', lw=2))
    # Rohan hand out in stop gesture
    ax.add_patch(patches.Polygon([[54, 130], [62, 130], [60, 120], [52, 120]], closed=True, fc='#E0A96D', ec='#0F172A', lw=1.5))
    ax.text(50, 158, "✋ 'BHAIYA RUKO!'", fontsize=10, fontweight='bold', color='#EF4444')
    
    # BOTTOM PANEL (Y: 26 to 96): Zoom Punch on Bunty's Terrified Face
    bot_panel = patches.Rectangle((4, 26), 100, 70, fc='#18181B', ec='#EF4444', lw=2.5)
    ax.add_patch(bot_panel)
    ax.text(8, 90, "REACTION: BUNTY'S BLUFF DETONATED", fontsize=9, fontweight='bold', color='#EF4444')
    
    # Large Vector Face of Bunty in Panic
    ax.add_patch(patches.Circle((54, 58), 20, fc='#D49B6A', ec='#0F172A', lw=3))
    # Eyes widening in shock behind sunglasses
    ax.add_patch(patches.Rectangle((40, 56), 28, 10, fc='#0F172A', ec='#EF4444', lw=2))
    # Wide open mouth in horror
    ax.add_patch(patches.Ellipse((54, 44), 10, 14, fc='#450A0A', ec='#0F172A', lw=2))
    
    # Stylized Vector Sweat Beads popping from brow
    ax.add_patch(patches.Circle((32, 72), 2.5, fc='#38BDF8', ec='#0F172A', lw=1.5))
    ax.add_patch(patches.Circle((28, 62), 1.8, fc='#38BDF8', ec='#0F172A', lw=1.5))
    ax.add_patch(patches.Circle((75, 70), 2.2, fc='#38BDF8', ec='#0F172A', lw=1.5))
    
    # Dynamic Action Lines (Shockwaves)
    for ang in [30, 60, 120, 150, 210, 240, 300, 330]:
        rad = np.radians(ang)
        x1, y1 = 54 + 23*np.cos(rad), 58 + 23*np.sin(rad)
        x2, y2 = 54 + 28*np.cos(rad), 58 + 28*np.sin(rad)
        ax.plot([x1, x2], [y1, y2], color='#EF4444', lw=2)
        
    ax.text(85, 45, "CYBER CELL\nPOLICE ALERT!", fontsize=8, fontweight='bold', color='#EF4444', ha='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#EF4444", lw=1.5))
            
    add_safe_zone_overlays(ax, 4, "The Counter-Trap & Bluff", "00:13.00 - 00:19.50")
    ax.text(54, 18.0, "ROHAN: 'Bhaiya ruko! Is scanner mein live photo verification hai...'", fontsize=9.2, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(54, 14.5, "scammer ka photo seedha police station jata hai!", fontsize=9.2, color='#F87171', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_04_split_bluff.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 4 rendered:", save_path)

def render_scene_5():
    # SCENE 5: THE CLIMAX / BRASS LADLE CHECKMATE (Bunty lunges, Kalu Bhaiya's ladle lands on shoulder)
    fig, ax = setup_canvas()
    
    # Background: Tea stall counter, steam, evening golden street lamps (#1E293B)
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#0F172A'))
    # Counter wooden barrier
    ax.add_patch(patches.Polygon([[0, 25], [108, 25], [108, 85], [0, 85]], closed=True, fc='#451A03', ec='#270F03', lw=2.5))
    
    # Stall QR board on counter
    ax.add_patch(patches.Rectangle((15, 85), 20, 26, fc='#E2E8F0', ec='#0F172A', lw=2))
    
    # BUNTY (Foreground Left - Lunging forward in desperation to grab sticker)
    torso_b = patches.Polygon([[20, 40], [45, 40], [50, 95], [25, 105]], closed=True, fc='#374151', ec='#0F172A', lw=3)
    ax.add_patch(torso_b)
    # Head crouched down
    ax.add_patch(patches.Circle((28, 118), 9, fc='#D49B6A', ec='#0F172A', lw=2.5))
    # Stretched arm reaching for QR sticker
    ax.add_patch(patches.Polygon([[28, 110], [18, 100], [14, 104], [25, 116]], closed=True, fc='#D49B6A', ec='#0F172A', lw=2))
    
    # KALU BHAIYA (Framed Right Half behind counter - Powerful calm presence)
    # Brown Vest & Cream Kurta
    torso_k = patches.Polygon([[65, 75], [98, 75], [96, 135], [62, 135]], closed=True, fc='#B45309', ec='#0F172A', lw=3)
    ax.add_patch(torso_k)
    # Red Gamchha on shoulder
    ax.add_patch(patches.Polygon([[62, 135], [72, 135], [70, 80], [60, 80]], closed=True, fc='#DC2626', ec='#0F172A', lw=2))
    # Head & Mustache
    ax.add_patch(patches.Rectangle((75, 133), 8, 8, fc='#C68642', ec='#0F172A', lw=2))
    ax.add_patch(patches.Circle((79, 149), 11, fc='#C68642', ec='#0F172A', lw=2.5))
    # Graying hair
    ax.add_patch(patches.Polygon([[70, 150], [72, 160], [86, 160], [88, 150], [85, 142], [73, 142]],
                                 closed=True, fc='#475569', ec='#0F172A', lw=2))
    # Thick Mustache
    ax.plot([72, 76, 79, 82, 86], [146, 148, 146, 148, 146], color='#0F172A', lw=3.5)
    # Calm knowing smile
    ax.plot([75, 79, 83], [143, 141, 143], color='#0F172A', lw=2)
    
    # HERO PROP: Long Brass Ladle landing firmly on Bunty's shoulder!
    # Hand holding ladle handle
    ax.add_patch(patches.Circle((66, 115), 4.5, fc='#C68642', ec='#0F172A', lw=2))
    # Long brass rod extending from Kalu across to Bunty's shoulder
    ax.plot([66, 38], [115, 102], color='#D97706', lw=4.5)
    # Polished Brass Cup resting on Bunty's shoulder
    ax.add_patch(patches.Circle((36, 101), 5.5, fc='#F59E0B', ec='#78350F', lw=2))
    
    # Impact vector star / clonk graphic
    ax.text(36, 108, "★ CLONK! ★", fontsize=9, fontweight='bold', color='#F59E0B', ha='center',
            bbox=dict(boxstyle="sawtooth,pad=0.3", fc="#FEF3C7", ec="#F59E0B", lw=1.5))
            
    add_safe_zone_overlays(ax, 5, "The Climax / Ladle Checkmate", "00:19.50 - 00:26.50")
    ax.text(54, 18.0, "KALU BHAIYA: 'Subah se teen hazaar rupaye gaye hain...'", fontsize=9.2, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(54, 14.5, "pehle hisaab kar, fir bhaagna beta!", fontsize=9.2, color='#34D399', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_05_ladle_climax.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 5 rendered:", save_path)

def render_scene_6():
    # SCENE 6: PUNCHLINE & CTA (Rohan raising cutting chai, Kalu smiling behind, CTA banner)
    fig, ax = setup_canvas()
    
    # Background: Warm vibrant tea stall ambience (#0F172A with amber glow)
    ax.add_patch(patches.Rectangle((0, 0), 108, 192, fc='#0F172A'))
    # Soft warm lighting glow
    ax.add_patch(patches.Circle((54, 120), 50, fc='#FEF08A', alpha=0.08))
    
    # Kalu Bhaiya in Background (Center-Left) smiling and wiping counter
    ax.add_patch(patches.Circle((32, 142), 9, fc='#C68642', ec='#0F172A', lw=2))
    ax.plot([26, 38], [139, 139], color='#0F172A', lw=3) # mustache
    ax.add_patch(patches.Polygon([[20, 95], [44, 95], [42, 134], [22, 134]], closed=True, fc='#B45309', ec='#0F172A', lw=2))
    ax.text(32, 155, "KALU BHAIYA", fontsize=7.5, fontweight='bold', color='#94A3B8', ha='center')
    
    # ROHAN (Foreground Center-Right - Celebratory Hero Stance)
    # Denim Jacket & Mustard Tee
    torso_r = patches.Polygon([[48, 45], [92, 45], [88, 115], [52, 115]], closed=True, fc='#1E3A8A', ec='#0F172A', lw=3)
    ax.add_patch(torso_r)
    ax.add_patch(patches.Polygon([[64, 115], [76, 115], [73, 102], [67, 102]], closed=True, fc='#F59E0B', ec='#0F172A', lw=1.8))
    # Head & Warm Engaging Smile
    ax.add_patch(patches.Rectangle((66, 114), 8, 8, fc='#E0A96D', ec='#0F172A', lw=2))
    ax.add_patch(patches.Circle((70, 130), 11, fc='#E0A96D', ec='#0F172A', lw=2.5))
    ax.add_patch(patches.Polygon([[60, 132], [64, 143], [78, 143], [82, 135], [80, 126], [72, 134], [61, 126]],
                                 closed=True, fc='#0F172A', ec='#0F172A', lw=2))
    # Cheerful Eyes & Confident Grin
    ax.plot([64, 69], [132, 132], color='#0F172A', lw=2)
    ax.plot([72, 77], [132, 132], color='#0F172A', lw=2)
    ax.plot([66, 70, 74], [122, 120, 122], color='#0F172A', lw=2.5) # broad smile
    
    # Hero Prop: Raising Hot Cutting Chai in Toast to Viewer!
    ax.add_patch(patches.Polygon([[54, 85], [50, 102], [58, 102], [60, 85]], closed=True, fc='#E0A96D', ec='#0F172A', lw=2))
    # Tea Glass
    ax.add_patch(patches.Polygon([[46, 102], [58, 102], [56, 125], [48, 125]], closed=True, fc='#60A5FA', ec='#1E3A8A', lw=2, alpha=0.6))
    ax.add_patch(patches.Polygon([[47, 103], [57, 103], [55, 118], [49, 118]], closed=True, fc='#D97706', ec='#B45309', lw=1.2))
    # Steam
    ax.plot([50, 52, 54], [126, 132, 138], color='#FEF3C7', lw=2, alpha=0.7)
    
    # CENTRAL VECTOR EDUCATIONAL BANNER (Above safe zone)
    cta_banner = patches.FancyBboxPatch((12, 52), 84, 18, boxstyle="round,pad=0.6",
                                        fc='#047857', ec='#34D399', lw=2.5)
    ax.add_patch(cta_banner)
    ax.text(54, 62, "💡 GOLDEN RULE OF UPI:", fontsize=9, fontweight='bold', color='#A7F3D0', ha='center')
    ax.text(54, 55.5, "SCAN SE PEHLE DUKAAN KA NAAM PADHO!", fontsize=10.5, fontweight='bold', color='#FFFFFF', ha='center')
    
    add_safe_zone_overlays(ax, 6, "The Punchline & CTA", "00:26.50 - 00:32.00")
    ax.text(54, 18.0, "ROHAN: 'Toh doston, UPI scan karte time dukaan ka naam zaroor check karo...'", fontsize=8.8, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(54, 14.5, "tech smart hai, tum bhi bano! #ChaiPeCharcha", fontsize=9.2, color='#38BDF8', ha='center')
    
    save_path = os.path.join(OUTPUT_DIR, "scene_06_rohan_punchline.png")
    plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Scene 6 rendered:", save_path)

if __name__ == '__main__':
    render_scene_1()
    render_scene_2()
    render_scene_3()
    render_scene_4()
    render_scene_5()
    render_scene_6()
    print("All 6 Scene Sample Frames successfully generated!")
