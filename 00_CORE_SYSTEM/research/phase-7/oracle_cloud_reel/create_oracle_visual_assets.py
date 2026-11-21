import os
from PIL import Image, ImageDraw, ImageFont

out_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\assets"
os.makedirs(out_dir, exist_ok=True)

# Colors
C_DARK_BG = (15, 23, 42, 255)      # Slate 900
C_CARD_BG = (30, 41, 59, 255)      # Slate 800
C_CARD_BORDER = (51, 65, 85, 255)  # Slate 700
C_ORACLE_RED = (239, 68, 68, 255)  # Red 500
C_NEON_CYAN = (6, 182, 212, 255)   # Cyan 500
C_EMERALD = (16, 185, 129, 255)    # Green 500
C_AMBER = (245, 158, 11, 255)      # Amber 500
C_WHITE = (255, 255, 255, 255)
C_MUTED = (148, 163, 184, 255)

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
font_body = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 30)
font_mono_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 32)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)

def create_warning_card():
    # Card 1: Oracle Instance Idle Warning
    w, h = 920, 520
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Outer Card
    draw.rounded_rectangle([0, 0, w, h], radius=24, fill=C_CARD_BG, outline=C_ORACLE_RED, width=4)
    
    # Header bar
    draw.rounded_rectangle([0, 0, w, 90], radius=24, fill=(55, 20, 25, 255))
    draw.text((40, 24), "⚠️  ORACLE CLOUD COMPUTE ALERT", font=font_subtitle, fill=C_ORACLE_RED)
    
    # Instance details
    draw.text((40, 120), "Instance: instance-2026-free (VM.Standard.A1.Flex)", font=font_body, fill=C_WHITE)
    draw.text((40, 165), "Shape: 4 OCPU, 24 GB RAM (Always Free)", font=font_body, fill=C_MUTED)
    
    # Status Alert Box
    draw.rounded_rectangle([40, 220, w - 40, 360], radius=16, fill=(38, 16, 20, 255), outline=C_ORACLE_RED, width=2)
    draw.text((65, 240), "IDLE RECLAMATION TRIGGERED!", font=font_subtitle, fill=C_ORACLE_RED)
    draw.text((65, 290), "Status: 7 Days CPU < 15% (Threshold: 20%)", font=font_body, fill=C_WHITE)
    draw.text((65, 325), "Action: Instance will be TERMINATED in 48 hrs!", font=font_body, fill=C_AMBER)
    
    # Bottom warning badge
    draw.rounded_rectangle([40, 400, w - 40, 480], radius=12, fill=(20, 30, 45, 255))
    draw.text((65, 425), "Data Loss Risk: HIGH (Boot Volume Deleted)", font=font_subtitle, fill=C_WHITE)
    
    im.save(os.path.join(out_dir, "card_warning.png"))
    print("Saved card_warning.png")

def create_cpu_gauge_card(cpu_val=8, status="DANGER (IDLE)"):
    w, h = 920, 440
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    draw.rounded_rectangle([0, 0, w, h], radius=24, fill=C_CARD_BG, outline=C_CARD_BORDER, width=3)
    draw.text((40, 30), "📊 OCI METRIC: 7-DAY CPU UTILIZATION", font=font_subtitle, fill=C_WHITE)
    
    # Gauge Bar Background
    bar_x, bar_y, bar_w, bar_h = 50, 120, w - 100, 60
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=30, fill=(45, 55, 72, 255))
    
    # 20% Threshold Marker Line
    t_x = bar_x + int(bar_w * 0.20)
    
    # Fill up to cpu_val
    fill_w = int(bar_w * (cpu_val / 100.0))
    fill_color = C_ORACLE_RED if cpu_val < 20 else C_EMERALD
    if fill_w > 0:
        draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=30, fill=fill_color)
    
    # Danger / Safe zone indicator
    draw.line([(t_x, bar_y - 15), (t_x, bar_y + bar_h + 15)], fill=C_AMBER, width=4)
    draw.text((t_x - 70, bar_y + bar_h + 25), "20% MIN LIMIT", font=font_badge, fill=C_AMBER)
    
    # Current Value Display
    draw.text((50, 250), f"Current Usage: {cpu_val}%", font=font_title, fill=fill_color)
    status_color = C_ORACLE_RED if cpu_val < 20 else C_EMERALD
    draw.text((50, 320), f"Status: {status}", font=font_subtitle, fill=status_color)
    draw.text((50, 370), "Oracle Policy: Must stay ABOVE 20% to avoid auto-deletion", font=font_body, fill=C_MUTED)
    
    im.save(os.path.join(out_dir, f"gauge_cpu_{cpu_val}.png"))
    print(f"Saved gauge_cpu_{cpu_val}.png")

def create_payg_card():
    # Card 3: Pay As You Go Comparison
    w, h = 920, 560
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    draw.rounded_rectangle([0, 0, w, h], radius=24, fill=C_CARD_BG, outline=C_EMERALD, width=4)
    draw.rounded_rectangle([0, 0, w, 90], radius=24, fill=(16, 50, 35, 255))
    draw.text((40, 24), "✅ METHOD 1: UPGRADE TO PAY-AS-YOU-GO", font=font_subtitle, fill=C_EMERALD)
    
    # Benefits checklist
    benefits = [
        ("💰 Cost For Always Free:", "Rs. 0 / Month ($0.00 Forever)"),
        ("⚡ Idle Instance Reclaim:", "100% IMMUNE (Never Terminated)"),
        ("🛡️ Account Tier:", "Paid Tier (Enterprise Priority)"),
        ("🚀 4 ARM Cores + 24GB RAM:", "Keeps Running Lifetime 24/7!")
    ]
    
    y = 120
    for label, val in benefits:
        draw.rounded_rectangle([40, y, w - 40, y + 80], radius=14, fill=(20, 30, 45, 255), outline=(40, 60, 85, 255), width=2)
        draw.text((60, y + 15), label, font=font_body, fill=C_MUTED)
        draw.text((60, y + 42), val, font=font_subtitle, fill=C_WHITE if "0" not in val else C_EMERALD)
        y += 100
        
    im.save(os.path.join(out_dir, "card_payg.png"))
    print("Saved card_payg.png")

def create_terminal_card():
    # Card 4: Terminal Window for lookbusy
    w, h = 920, 540
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Terminal Background
    draw.rounded_rectangle([0, 0, w, h], radius=20, fill=(10, 15, 26, 255), outline=C_CARD_BORDER, width=3)
    
    # Header with traffic lights
    draw.rounded_rectangle([0, 0, w, 60], radius=20, fill=(20, 28, 44, 255))
    draw.ellipse([25, 20, 45, 40], fill=(239, 68, 68, 255))
    draw.ellipse([55, 20, 75, 40], fill=(245, 158, 11, 255))
    draw.ellipse([85, 20, 105, 40], fill=(16, 185, 129, 255))
    draw.text((320, 18), "ubuntu@oracle-free-vm:~", font=font_badge, fill=C_MUTED)
    
    # Terminal Lines
    lines = [
        ("$ sudo apt update && sudo apt install -y curl", C_WHITE),
        ("# Step 1: Install Keep-Alive Daemon", C_NEON_CYAN),
        ("$ curl -sL https://raw.githubusercontent.com/... | bash", C_WHITE),
        ("# Step 2: Keep CPU at steady 22% (Safe Zone)", C_NEON_CYAN),
        ("$ lookbusy -c 22 -m 128MB --quiet &", (250, 204, 21, 255)),
        ("[OK] Background worker running. CPU locked at 22%.", C_EMERALD),
        ("[OCI-SHIELD] Idle Reclaim Status: PROTECTED", C_EMERALD)
    ]
    
    y = 85
    for line, col in lines:
        draw.text((35, y), line, font=font_mono, fill=col)
        y += 58
        
    im.save(os.path.join(out_dir, "card_terminal.png"))
    print("Saved card_terminal.png")

create_warning_card()
create_cpu_gauge_card(cpu_val=6, status="CRITICAL DANGER (< 20%)")
create_cpu_gauge_card(cpu_val=24, status="PROTECTED & SAFE (> 20%)")
create_payg_card()
create_terminal_card()
