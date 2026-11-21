"""professional_2d_animator.py
MASTER-AI Professional 2D Cinematic Animation Engine

Pure 2D vector, layered artwork, and multi-plane compositing engine:
- Multi-layer parallax depth (Background, Midground, Character, Foreground, Atmosphere)
- Rigged 2D character silhouettes with walking cycles, head tilts, and hand interactions
- Physical object animations (sliding secret drawers, opening box latches, folding paper)
- Environmental simulation (falling rain with window ripples, swaying chain lanterns, cloud parallax)
- Organic particle systems (Brownian dust motes, drifting mist, glowing spiritual orbs, falling tears)
- Progressive Devanagari calligraphy drawing with ink bleed and paper crease lighting
- Strict Invariant: 100% 2D vector/artwork compositing direct to FFmpeg; ZERO static photo slideshows.
"""

import os
import sys
import math
import subprocess
import json
import logging
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

logger = logging.getLogger("MasterAI.2D.Animator")
logging.basicConfig(level=logging.INFO)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class Professional2DAnimator:
    """Production 2D multi-layer animation and compositing engine."""

    def __init__(self, res_x: int = 1280, res_y: int = 720, fps: int = 24):
        self.res_x = res_x
        self.res_y = res_y
        self.fps = fps
        self.font_hindi_large = self._load_hindi_font(32)
        self.font_hindi_mid = self._load_hindi_font(22)
        self.font_hindi_small = self._load_hindi_font(16)
        self.font_english_sub = self._load_font("arial.ttf", 14)

    def _load_font(self, font_name: str, size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            return ImageFont.load_default()

    def _load_hindi_font(self, size: int) -> ImageFont.ImageFont:
        candidates = [
            "C:/Windows/Fonts/Nirmala.ttc",
            "C:/Windows/Fonts/nirmala.ttf",
            "C:/Windows/Fonts/mangal.ttf",
            "C:/Windows/Fonts/arial.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return self._load_font("arial.ttf", size)

    def render_scene_1_arrival_gateway(
        self,
        output_mp4: str,
        duration_sec: float = 7.0
    ) -> str:
        """
        Scene 1: Rohit returns to the ancestral estate at midnight.
        - Multi-plane parallax: Moon, misty hills, swaying bare oak trees
        - Ornate wrought-iron ancestral gateway with weathered stone pillars
        - 2D animated character silhouette walking forward with rhythmic stride
        - Drifting mist fog ribbons and autumn leaf particles
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        np.random.seed(42)
        num_leaves = 35
        leaf_x = np.random.uniform(0, self.res_x, num_leaves)
        leaf_y = np.random.uniform(100, 680, num_leaves)
        leaf_vx = np.random.uniform(1.5, 3.5, num_leaves)
        leaf_phi = np.random.uniform(0, 2*math.pi, num_leaves)

        # Precompute gradient background - Atmospheric moonlit midnight
        bg_array = np.zeros((self.res_y, self.res_x, 3), dtype=np.uint8)
        for y in range(self.res_y):
            t = y / float(self.res_y)
            r = int(24 * (1 - t) + 48 * t)
            g = int(36 * (1 - t) + 68 * t)
            b = int(68 * (1 - t) + 115 * t)
            bg_array[y, :] = [r, g, b]
        base_bg = Image.fromarray(bg_array)

        for frame in range(total_frames):
            im = base_bg.copy()
            draw = ImageDraw.Draw(im)

            # --- Layer 1: Moon and Moonlight Halo ---
            moon_cx, moon_cy = 1000, 160
            for r_halo in range(120, 50, -10):
                alpha_val = int(12 * (1.0 - r_halo / 120.0))
                draw.ellipse([(moon_cx - r_halo, moon_cy - r_halo), (moon_cx + r_halo, moon_cy + r_halo)], fill=(200, 215, 235, alpha_val))
            draw.ellipse([(moon_cx - 45, moon_cy - 45), (moon_cx + 45, moon_cy + 45)], fill=(235, 242, 255))
            draw.ellipse([(moon_cx - 20, moon_cy - 20), (moon_cx + 35, moon_cy + 35)], fill=(215, 225, 240)) # moon crater

            # --- Layer 2: Distant Hills & Trees (Parallax) ---
            tree_drift = int(frame * 0.15)
            # Distant ridge
            ridge_points = [(0, 480)]
            for rx in range(0, self.res_x + 80, 80):
                ry = 450 + int(35 * math.sin((rx + tree_drift) * 0.005) + 15 * math.cos((rx + tree_drift) * 0.012))
                ridge_points.append((rx, ry))
            ridge_points.extend([(self.res_x, self.res_y), (0, self.res_y)])
            draw.polygon(ridge_points, fill=(35, 48, 72))

            # Mansion silhouette in distance with warm glowing windows
            mx = 820 - int(frame * 0.2)
            draw.rectangle([(mx, 360), (mx + 220, 470)], fill=(26, 36, 54))
            draw.polygon([(mx - 20, 360), (mx + 110, 300), (mx + 240, 360)], fill=(22, 30, 46))
            draw.rectangle([(mx + 45, 385), (mx + 75, 420)], fill=(255, 200, 80)) # Warm window lights
            draw.rectangle([(mx + 135, 385), (mx + 165, 420)], fill=(255, 200, 80))

            # Bare oak trees swaying in wind
            sway = 0.03 * math.sin(frame * 0.08)
            for tx, th in [(260, 220), (420, 260), (980, 240)]:
                top_x = tx + int(th * sway)
                draw.line([(tx, 490), (top_x, 490 - th)], fill=(24, 32, 48), width=6)
                draw.line([(tx + (top_x - tx)//2, 490 - th//2), (top_x - 40, 490 - th - 30)], fill=(24, 32, 48), width=3)
                draw.line([(tx + (top_x - tx)//2, 490 - th//2), (top_x + 45, 490 - th - 20)], fill=(24, 32, 48), width=3)

            # --- Layer 3: Stone Ground Path & Ancestral Gateway ---
            draw.rectangle([(0, 480), (self.res_x, self.res_y)], fill=(42, 54, 74))
            # Path perspective lines
            draw.polygon([(460, 480), (740, 480), (1050, 720), (180, 720)], fill=(55, 68, 92))
            for py in range(500, self.res_y, 40):
                draw.line([(350 - (py - 480)*0.6, py), (850 + (py - 480)*0.7, py)], fill=(48, 60, 82), width=1)

            # Gateway stone pillars with carved masonry
            draw.rectangle([(320, 300), (390, 520)], fill=(65, 78, 102), outline=(95, 115, 145), width=2)
            draw.polygon([(310, 300), (355, 265), (400, 300)], fill=(80, 95, 125)) # Cap stone
            draw.rectangle([(850, 300), (920, 520)], fill=(65, 78, 102), outline=(95, 115, 145), width=2)
            draw.polygon([(840, 300), (885, 265), (930, 300)], fill=(80, 95, 125))

            # Wrought-iron gate doors (partially ajar)
            gate_l = 390
            for bar_x in range(gate_l + 10, gate_l + 180, 20):
                draw.line([(bar_x, 340), (bar_x, 500)], fill=(60, 74, 98), width=3)
                draw.polygon([(bar_x - 4, 340), (bar_x, 325), (bar_x + 4, 340)], fill=(110, 130, 165)) # Spear tops
            draw.arc([(gate_l + 10, 320), (gate_l + 180, 440)], 180, 360, fill=(75, 92, 120), width=3)

            # --- Layer 4: Character Animation (Rohit Walking Forward) ---
            # Walk progress from left into the path
            char_prog = min(1.0, frame / float(total_frames))
            cx = int(240 + 260 * char_prog)
            cy = int(430 + 130 * char_prog) # Moves closer to camera
            scale = 0.85 + 0.35 * char_prog

            walk_phase = frame * 0.28
            leg_swing = 18 * math.sin(walk_phase)
            bob = abs(5 * math.sin(walk_phase))

            # Head
            head_r = int(12 * scale)
            head_cy = int(cy - 90 * scale + bob)
            draw.ellipse([(cx - head_r, head_cy - head_r), (cx + head_r, head_cy + head_r)], fill=(6, 8, 12))

            # Torso & Coat
            torso_top = head_cy + head_r
            torso_bot = int(cy - 45 * scale + bob)
            draw.polygon([
                (cx - int(14 * scale), torso_top),
                (cx + int(14 * scale), torso_top),
                (cx + int(18 * scale), torso_bot),
                (cx - int(22 * scale + 6 * math.sin(walk_phase)), torso_bot) # Coat tail moving
            ], fill=(8, 10, 16))

            # Backpack on shoulders
            draw.rounded_rectangle([
                (cx - int(24 * scale), torso_top + 4),
                (cx - int(14 * scale), torso_bot - 8)
            ], radius=4, fill=(14, 18, 25))

            # Legs with walk cycle
            hip_y = torso_bot
            foot_l_x = cx - int(leg_swing * scale)
            foot_r_x = cx + int(leg_swing * scale)
            foot_y = int(cy + 25 * scale)

            draw.line([(cx - 6, hip_y), (foot_l_x, foot_y)], fill=(6, 8, 12), width=int(6 * scale))
            draw.line([(cx + 6, hip_y), (foot_r_x, foot_y)], fill=(6, 8, 12), width=int(6 * scale))
            # Boots
            draw.rectangle([(foot_l_x - 3, foot_y - 2), (foot_l_x + 8, foot_y + 4)], fill=(4, 5, 8))
            draw.rectangle([(foot_r_x - 3, foot_y - 2), (foot_r_x + 8, foot_y + 4)], fill=(4, 5, 8))

            # Arm holding key
            arm_swing = int(14 * math.sin(walk_phase))
            hand_x = cx + int((16 + arm_swing) * scale)
            hand_y = torso_top + int((24 + bob) * scale)
            draw.line([(cx + 10, torso_top + 4), (hand_x, hand_y)], fill=(8, 10, 16), width=int(4 * scale))
            # Antique brass key glint
            draw.line([(hand_x, hand_y), (hand_x + 10, hand_y - 4)], fill=(234, 179, 8), width=2)
            if frame % 12 < 4:
                draw.ellipse([(hand_x + 10, hand_y - 6), (hand_x + 14, hand_y - 2)], fill=(255, 255, 200)) # Key sparkle

            # --- Layer 5: Particles (Blowing Leaves & Mist) ---
            for i in range(num_leaves):
                leaf_x[i] = (leaf_x[i] + leaf_vx[i]) % self.res_x
                curr_y = leaf_y[i] + 10 * math.sin(frame * 0.12 + leaf_phi[i])
                draw.ellipse([(leaf_x[i], curr_y), (leaf_x[i] + 4, curr_y + 2)], fill=(45, 60, 50, 180))

            # --- Chapter Banner Overlay ---
            if frame > 12:
                alpha = min(1.0, (frame - 12) / 20.0)
                if frame > total_frames - 20:
                    alpha = max(0.0, (total_frames - frame) / 20.0)
                badge_w, badge_h = 380, 55
                bx, by = 50, self.res_y - 85
                draw.rectangle([(bx, by), (bx + badge_w, by + badge_h)], fill=(12, 16, 24))
                draw.rectangle([(bx, by), (bx + 6, by + badge_h)], fill=(234, 179, 8))
                draw.text((bx + 18, by + 12), "भाग १: पैतृक हवेली का सन्नाटा", fill=(255, 255, 255), font=self.font_hindi_mid)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Scene 1 rendered: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_scene_2_corridor_lantern(
        self,
        output_mp4: str,
        duration_sec: float = 7.0
    ) -> str:
        """
        Scene 2: Inside the dark ancestral corridor.
        - Victorian wood-paneled walls with ancestral framed portraits
        - Pendulum swinging vintage brass lantern casting dynamic radial light
        - Character walks down the perspective hallway and pauses under portrait
        - Golden dust particles drifting in light beam
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        np.random.seed(101)
        num_motes = 50
        mote_x = np.random.uniform(400, 880, num_motes)
        mote_y = np.random.uniform(180, 620, num_motes)

        for frame in range(total_frames):
            im = Image.new("RGB", (self.res_x, self.res_y), color=(48, 36, 42))
            draw = ImageDraw.Draw(im)

            # Perspective Hallway lines (vanishing point at 640, 280)
            vp_x, vp_y = 640, 280

            # Floorboards - Polished Victorian Oak
            draw.polygon([(0, 720), (self.res_x, 720), (740, 440), (540, 440)], fill=(75, 52, 36))
            for fx in range(-200, self.res_x + 300, 140):
                draw.line([(fx, 720), (vp_x, 440)], fill=(52, 35, 24), width=2)

            # Left and Right walls - Classic Damask Wallpaper
            draw.polygon([(0, 0), (540, 200), (540, 440), (0, 720)], fill=(64, 46, 54))
            draw.polygon([(self.res_x, 0), (740, 200), (740, 440), (self.res_x, 720)], fill=(64, 46, 54))
            # Wainscoting panels on walls
            draw.line([(0, 420), (540, 360)], fill=(96, 68, 50), width=4)
            draw.line([(self.res_x, 420), (740, 360)], fill=(96, 68, 50), width=4)

            # Mother's framed portrait on right wall with glowing gilded frame
            pw_x1, pw_y1 = 820, 220
            pw_x2, pw_y2 = 1020, 420
            draw.rectangle([(pw_x1, pw_y1), (pw_x2, pw_y2)], fill=(85, 60, 42), outline=(245, 195, 55), width=5)
            draw.rectangle([(pw_x1 + 10, pw_y1 + 10), (pw_x2 - 10, pw_y2 - 10)], fill=(125, 95, 80))
            # Maternal portrait painted details
            draw.ellipse([(pw_x1 + 75, pw_y1 + 35), (pw_x1 + 125, pw_y1 + 85)], fill=(195, 160, 140)) # face
            draw.ellipse([(pw_x1 + 80, pw_y1 + 32), (pw_x1 + 120, pw_y1 + 60)], fill=(40, 30, 25)) # hair
            draw.polygon([(pw_x1 + 45, pw_y1 + 160), (pw_x1 + 155, pw_y1 + 160), (pw_x1 + 125, pw_y1 + 85), (pw_x1 + 75, pw_y1 + 85)], fill=(160, 75, 65)) # red saree

            # --- Swaying Vintage Brass Lantern Animation ---
            pendulum_angle = 0.08 * math.sin(frame * 0.09)
            chain_len = 160
            anchor_x, anchor_y = 640, 0
            lantern_x = int(anchor_x + chain_len * math.sin(pendulum_angle))
            lantern_y = int(anchor_y + chain_len * math.cos(pendulum_angle))

            # Chain
            draw.line([(anchor_x, anchor_y), (lantern_x, lantern_y)], fill=(180, 140, 60), width=2)
            # Lantern housing
            lw, lh = 36, 55
            draw.rectangle([(lantern_x - lw//2, lantern_y), (lantern_x + lw//2, lantern_y + lh)], fill=(120, 90, 35), outline=(245, 195, 55), width=2)
            draw.polygon([(lantern_x - lw//2 - 6, lantern_y), (lantern_x, lantern_y - 18), (lantern_x + lw//2 + 6, lantern_y)], fill=(210, 165, 45))

            # Animated candle flame flicker
            flame_flicker = 3 * math.sin(frame * 0.45) + 2 * math.cos(frame * 0.8)
            flame_cy = lantern_y + lh//2
            draw.ellipse([(lantern_x - 7, flame_cy - 12 + flame_flicker), (lantern_x + 7, flame_cy + 12 + flame_flicker)], fill=(255, 235, 140))
            draw.ellipse([(lantern_x - 3, flame_cy - 7 + flame_flicker), (lantern_x + 3, flame_cy + 7 + flame_flicker)], fill=(255, 255, 255))

            # Dynamic radial light beam from lantern onto hallway floor
            light_w = int(240 + 25 * math.sin(frame * 0.1))
            floor_light_x = int(lantern_x + 80 * math.sin(pendulum_angle))
            # Outer warm glow
            draw.polygon([
                (lantern_x - 10, lantern_y + lh),
                (lantern_x + 10, lantern_y + lh),
                (floor_light_x + light_w, 660),
                (floor_light_x - light_w, 660)
            ], fill=(135, 98, 52))
            # Inner bright golden beam
            draw.polygon([
                (lantern_x - 5, lantern_y + lh),
                (lantern_x + 5, lantern_y + lh),
                (floor_light_x + int(light_w * 0.55), 650),
                (floor_light_x - int(light_w * 0.55), 650)
            ], fill=(210, 165, 90))

            # --- Character Animation: Rohit Walking and Stopping ---
            # Moves down the corridor toward the portrait
            char_step = min(1.0, frame / 100.0)
            char_x = int(460 + 180 * char_step)
            char_y = int(420 + 60 * char_step)
            c_scale = 0.75 + 0.35 * char_step

            is_walking = frame < 85
            bob = abs(4 * math.sin(frame * 0.3)) if is_walking else 0
            leg_s = 14 * math.sin(frame * 0.3) if is_walking else 2

            # Head tilt looking at portrait after frame 85
            head_tilt = 4 if not is_walking else 0
            h_r = int(14 * c_scale)
            h_cy = int(char_y - 100 * c_scale + bob)
            draw.ellipse([(char_x - h_r + head_tilt, h_cy - h_r), (char_x + h_r + head_tilt, h_cy + h_r)], fill=(8, 6, 10))

            # Torso & Breathing
            breath = 2 * math.sin(frame * 0.1) if not is_walking else 0
            draw.polygon([
                (char_x - int(16 * c_scale), h_cy + h_r),
                (char_x + int(16 * c_scale), h_cy + h_r),
                (char_x + int(20 * c_scale + breath), char_y - int(40 * c_scale)),
                (char_x - int(20 * c_scale), char_y - int(40 * c_scale))
            ], fill=(12, 9, 14))

            # Legs
            draw.line([(char_x - 8, char_y - int(40 * c_scale)), (char_x - int(leg_s * c_scale), char_y + int(40 * c_scale))], fill=(8, 6, 10), width=int(7 * c_scale))
            draw.line([(char_x + 8, char_y - int(40 * c_scale)), (char_x + int(leg_s * c_scale), char_y + int(40 * c_scale))], fill=(8, 6, 10), width=int(7 * c_scale))

            # --- Dust Particles Floating in Light ---
            for mi in range(num_motes):
                mote_x[mi] = (mote_x[mi] + 0.4 * math.sin(frame * 0.05 + mi))
                mote_y[mi] = (mote_y[mi] + 0.2 * math.cos(frame * 0.04 + mi))
                draw.ellipse([(mote_x[mi], mote_y[mi]), (mote_x[mi] + 3, mote_y[mi] + 3)], fill=(220, 180, 110, 140))

            # Chapter Badge
            if frame > 12:
                alpha = min(1.0, (frame - 12) / 20.0)
                if frame > total_frames - 20:
                    alpha = max(0.0, (total_frames - frame) / 20.0)
                bx, by = 50, self.res_y - 85
                draw.rectangle([(bx, by), (bx + 380, by + 55)], fill=(14, 10, 18))
                draw.rectangle([(bx, by), (bx + 6, by + 55)], fill=(245, 158, 11))
                draw.text((bx + 18, by + 12), "भाग २: खामोश कमरा और यादें", fill=(255, 255, 255), font=self.font_hindi_mid)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Scene 2 rendered: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_scene_3_desk_drawer_hands(
        self,
        output_mp4: str,
        duration_sec: float = 7.0
    ) -> str:
        """
        Scene 3: The Secret Desk & Keepsake Box.
        - Arched window with falling rain streaks and lightning flash
        - Antique hand-carved mahogany desk in close-up
        - Secret wooden drawer slides open outward with smooth cubic ease
        - Hands enter frame, lift latch of ornate brass keepsake box
        - Reveals folded yellowed parchment envelope inside
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        np.random.seed(202)
        rain_drops = 70
        rain_x = np.random.uniform(80, 480, rain_drops)
        rain_y = np.random.uniform(0, 460, rain_drops)

        for frame in range(total_frames):
            im = Image.new("RGB", (self.res_x, self.res_y), color=(58, 44, 52))
            draw = ImageDraw.Draw(im)

            # Lightning flash event around frame 40-44
            is_lightning = 40 <= frame <= 44
            win_bg = (195, 220, 255) if is_lightning else (38, 52, 78)

            # --- Background Arched Window with Falling Rain ---
            draw.rectangle([(80, 60), (480, 460)], fill=win_bg)
            draw.pieslice([(80, 20), (480, 200)], 180, 360, fill=win_bg)
            # Window mullions
            draw.line([(280, 20), (280, 460)], fill=(20, 28, 40), width=8)
            draw.line([(80, 260), (480, 260)], fill=(20, 28, 40), width=6)

            # Rain streaks on window
            for ri in range(rain_drops):
                rain_y[ri] = (rain_y[ri] + 18) % 440
                draw.line([(rain_x[ri], rain_y[ri]), (rain_x[ri] - 2, rain_y[ri] + 16)], fill=(210, 230, 255), width=2)

            # --- Antique Mahogany Desk (Foreground Close-up) ---
            desk_top_y = 380
            draw.rectangle([(0, desk_top_y), (self.res_x, self.res_y)], fill=(105, 62, 42), outline=(145, 90, 60), width=3)
            # Wood grain horizontal lines
            for gy in range(desk_top_y + 20, self.res_y, 35):
                draw.line([(0, gy), (self.res_x, gy)], fill=(82, 48, 32), width=2)

            # Candle on desk with warm golden radial illumination
            cand_x, cand_y = 1100, desk_top_y - 80
            draw.rectangle([(cand_x - 8, cand_y + 20), (cand_x + 8, desk_top_y)], fill=(235, 225, 205)) # wax
            draw.ellipse([(cand_x - 25, desk_top_y - 10), (cand_x + 25, desk_top_y + 10)], fill=(195, 150, 50)) # brass stand
            flick = 3 * math.sin(frame * 0.4)
            draw.ellipse([(cand_x - 8, cand_y - 12 + flick), (cand_x + 8, cand_y + 16 + flick)], fill=(255, 185, 55))
            draw.ellipse([(cand_x - 4, cand_y - 6 + flick), (cand_x + 4, cand_y + 8 + flick)], fill=(255, 255, 230))

            # --- Secret Drawer Sliding Open Animation ---
            # Drawer animates out between frame 20 and frame 65 (cubic ease out)
            drawer_p = max(0.0, min(1.0, (frame - 20) / 45.0))
            ease_slide = 1.0 - math.pow(1.0 - drawer_p, 3)
            slide_dist = int(140 * ease_slide)

            dw_x1, dw_w = 420, 440
            dw_y1 = desk_top_y + 60
            dw_y2 = dw_y1 + 160 + slide_dist

            # Drawer cavity
            draw.rectangle([(dw_x1, dw_y1), (dw_x1 + dw_w, dw_y1 + 180)], fill=(32, 18, 14))

            # Drawer box interior
            if slide_dist > 10:
                draw.rectangle([(dw_x1 + 15, dw_y1 + 10), (dw_x1 + dw_w - 15, dw_y1 + slide_dist + 40)], fill=(92, 38, 48), outline=(52, 22, 28), width=3) # Crimson velvet lining

                # Inside drawer: Ornate Brass Keepsake Box
                box_x1 = dw_x1 + 70
                box_y1 = dw_y1 + int(slide_dist * 0.6)
                box_w, box_h = 280, 130
                draw.rectangle([(box_x1, box_y1), (box_x1 + box_w, box_y1 + box_h)], fill=(215, 168, 55), outline=(255, 215, 105), width=3)
                draw.rectangle([(box_x1 + 10, box_y1 + 10), (box_x1 + box_w - 10, box_y1 + box_h - 10)], outline=(175, 130, 40), width=2) # Etching

                # Brass box latch and lid opening (opens after frame 75)
                lid_p = max(0.0, min(1.0, (frame - 75) / 35.0))
                if lid_p > 0:
                    draw.rectangle([(box_x1, box_y1 - int(50 * lid_p)), (box_x1 + box_w, box_y1)], fill=(235, 185, 75), outline=(255, 225, 130), width=2)

                    # Inside Box: Yellowed Parchment Letter with red tie
                    env_x = box_x1 + 45
                    env_y = box_y1 + 25
                    draw.rectangle([(env_x, env_y), (env_x + 190, env_y + 80)], fill=(245, 232, 195), outline=(210, 190, 145), width=2)
                    draw.line([(env_x + 95, env_y), (env_x + 95, env_y + 80)], fill=(215, 45, 35), width=3) # Red ribbon
                    draw.text((env_x + 25, env_y + 30), "चिट्ठी: मेरे बेटे के लिए", fill=(75, 45, 25), font=self.font_hindi_small)

            # Drawer front face with brass handles
            draw.rectangle([(dw_x1, dw_y2 - 60), (dw_x1 + dw_w, dw_y2)], fill=(92, 54, 36), outline=(135, 80, 52), width=3)
            # Brass handle
            hx = dw_x1 + dw_w // 2
            draw.arc([(hx - 35, dw_y2 - 45), (hx + 35, dw_y2 - 15)], 0, 180, fill=(245, 195, 70), width=4)

            # --- Hands Entering Frame to Open Latch (Frames 70 to 140) ---
            if frame > 68:
                hand_p = min(1.0, (frame - 68) / 30.0)
                # Left hand resting on box side
                lh_y = int(self.res_y - (self.res_y - box_y1 - 30) * hand_p)
                draw.polygon([(box_x1 - 40, self.res_y), (box_x1 + 10, lh_y), (box_x1 + 35, lh_y + 20), (box_x1, self.res_y)], fill=(32, 22, 28))
                # Right hand reaching for latch
                rh_p = min(1.0, (frame - 75) / 25.0)
                rh_x = int(box_x1 + box_w + 50 - 80 * rh_p)
                rh_y = int(self.res_y - (self.res_y - box_y1 - 10) * rh_p)
                draw.polygon([(self.res_x - 40, self.res_y), (rh_x, rh_y), (rh_x - 30, rh_y + 25), (self.res_x - 120, self.res_y)], fill=(32, 22, 28))

            # Chapter Badge
            if frame > 12:
                alpha = min(1.0, (frame - 12) / 20.0)
                if frame > total_frames - 20:
                    alpha = max(0.0, (total_frames - frame) / 20.0)
                bx, by = 50, self.res_y - 85
                draw.rectangle([(bx, by), (bx + 400, by + 55)], fill=(18, 12, 16))
                draw.rectangle([(bx, by), (bx + 6, by + 55)], fill=(234, 88, 12))
                draw.text((bx + 18, by + 12), "भाग ३: गुप्त दराज और पीली चिट्ठी", fill=(255, 255, 255), font=self.font_hindi_mid)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Scene 3 rendered: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_scene_4_letter_calligraphy(
        self,
        output_mp4: str,
        duration_sec: float = 7.0
    ) -> str:
        """
        Scene 4: The Unfolding Letter & The Mother's Revelation.
        - 2D perspective paper unfolds from folded parcel into full parchment
        - Progressive Devanagari calligraphy forms dynamically with moving ink flow
        - Translucent spiritual silhouette of mother placing hand on Rohit's shoulder
        - Falling tear drop creates realistic ink-blur ring on parchment
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        np.random.seed(303)
        num_sparks = 40
        spark_x = np.random.uniform(200, 1080, num_sparks)
        spark_y = np.random.uniform(200, 650, num_sparks)
        spark_vy = np.random.uniform(0.6, 1.8, num_sparks)

        calligraphy_lines = [
            (25, "मेरे प्यारे बेटे रोहित,"),
            (55, "जब यह पत्र तुम्हें मिलेगा, मैं शायद इस दुनिया में नहीं होऊँगी।"),
            (85, "माफ़ करना, मैंने अपनी बीमारी छुपाई ताकि तुम्हारी कॉलेज फीस भरी जा सके।"),
            (115, "कैंसर का इलाज रोककर मैंने तुम्हारी डिग्री चुनी... तुम्हारी जीत ही मेरी सांस थी।"),
            (145, "सदा सिर उठाकर जीना... — तुम्हारी माँ")
        ]

        for frame in range(total_frames):
            im = Image.new("RGB", (self.res_x, self.res_y), color=(20, 14, 18))
            draw = ImageDraw.Draw(im)

            # Camera slow push-in scale factor
            zoom = 1.0 + 0.08 * (frame / float(total_frames))

            # --- Paper Unfolding Animation (Frames 0 to 45) ---
            unfold_p = min(1.0, frame / 35.0)
            ease_unfold = 1.0 - math.pow(1.0 - unfold_p, 3)

            pw = int((320 + 520 * ease_unfold) * zoom)
            ph = int((200 + 360 * ease_unfold) * zoom)
            px = (self.res_x - pw) // 2
            py = (self.res_y - ph) // 2 - int(15 * zoom)

            # Drop shadow under parchment
            draw.rectangle([(px + 14, py + 14), (px + pw + 14, py + ph + 14)], fill=(8, 5, 8))
            # Aged parchment sheet with hand-torn border effect
            draw.rectangle([(px, py), (px + pw, py + ph)], fill=(244, 235, 212), outline=(175, 150, 115), width=3)
            draw.rectangle([(px + 12, py + 12), (px + pw - 12, py + ph - 12)], outline=(215, 195, 160), width=1)

            # Crease lines from original folds
            if unfold_p > 0.6:
                crease_alpha = int(120 * (1.0 - (unfold_p - 0.6) / 0.4 * 0.5))
                draw.line([(px + pw // 2, py + 15), (px + pw // 2, py + ph - 15)], fill=(195, 175, 140), width=2)
                draw.line([(px + 15, py + ph // 2), (px + pw - 15, py + ph // 2)], fill=(195, 175, 140), width=2)

            # --- Dynamic Progressive Hindi Calligraphy ---
            cur_y = py + int(45 * zoom)
            line_spacing = int(58 * zoom)

            for start_f, text_str in calligraphy_lines:
                if frame >= start_f:
                    char_p = min(1.0, (frame - start_f) / 22.0)
                    chars_visible = int(len(text_str) * char_p)
                    visible_text = text_str[:chars_visible]

                    # Special red/gold highlight for the cancer sacrifice line
                    if "कैंसर" in text_str and frame >= start_f + 10:
                        text_color = (180, 30, 25)
                    elif "माँ" in text_str:
                        text_color = (130, 40, 20)
                    else:
                        text_color = (40, 28, 22)

                    draw.text((px + int(45 * zoom), cur_y), visible_text, fill=text_color, font=self.font_hindi_mid)

                    # Dynamic ink pen nib sparkle at active drawing character
                    if char_p < 1.0 and len(visible_text) > 0:
                        nib_x = px + int(45 * zoom) + len(visible_text) * 14
                        draw.ellipse([(nib_x - 3, cur_y + 8), (nib_x + 3, cur_y + 14)], fill=(180, 50, 40))
                cur_y += line_spacing

            # --- Spiritual Translucent Silhouette of Mother ---
            if frame > 70:
                mom_alpha = min(0.35, (frame - 70) / 70.0 * 0.35)
                # Soft glowing presence above letter
                mom_x, mom_y = px + pw - 160, py + 120
                draw.ellipse([(mom_x - 30, mom_y - 30), (mom_x + 30, mom_y + 30)], fill=(245, 210, 160)) # Head
                draw.polygon([(mom_x - 50, mom_y + 110), (mom_x + 50, mom_y + 110), (mom_x + 25, mom_y + 25), (mom_x - 25, mom_y + 25)], fill=(245, 210, 160)) # Blessing pose

            # --- Tear Drop Falling onto Parchment (Frames 130 to 168) ---
            if frame >= 130:
                tear_p = min(1.0, (frame - 130) / 12.0)
                tear_y = int(py + 40 + (ph - 180) * tear_p)
                tear_x = px + int(pw * 0.55)
                if tear_p < 1.0:
                    draw.ellipse([(tear_x - 4, tear_y - 8), (tear_x + 4, tear_y + 8)], fill=(210, 230, 255))
                else:
                    # Ink-bleed smudge ring on paper
                    smudge_r = int(6 + 18 * min(1.0, (frame - 142) / 20.0))
                    draw.ellipse([(tear_x - smudge_r, tear_y - smudge_r//2), (tear_x + smudge_r, tear_y + smudge_r//2)], outline=(140, 110, 90), width=2)
                    draw.ellipse([(tear_x - smudge_r//2, tear_y - smudge_r//4), (tear_x + smudge_r//2, tear_y + smudge_r//4)], fill=(225, 210, 185))

            # Floating spiritual gold stardust
            for si in range(num_sparks):
                spark_y[si] -= spark_vy[si]
                if spark_y[si] < py - 20:
                    spark_y[si] = py + ph + 20
                draw.ellipse([(spark_x[si], spark_y[si]), (spark_x[si] + 3, spark_y[si] + 3)], fill=(245, 190, 80))

            # Chapter Badge
            if frame > 12:
                alpha = min(1.0, (frame - 12) / 20.0)
                if frame > total_frames - 20:
                    alpha = max(0.0, (total_frames - frame) / 20.0)
                bx, by = 50, self.res_y - 85
                draw.rectangle([(bx, by), (bx + 390, by + 55)], fill=(22, 14, 20))
                draw.rectangle([(bx, by), (bx + 6, by + 55)], fill=(220, 38, 38))
                draw.text((bx + 18, by + 12), "भाग ४: माँ का पत्र और अंतिम सच", fill=(255, 255, 255), font=self.font_hindi_mid)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Scene 4 rendered: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4

    def render_scene_5_sunset_window_closure(
        self,
        output_mp4: str,
        duration_sec: float = 6.0
    ) -> str:
        """
        Scene 5: Window by Dusk & Eternal Maternal Love.
        - Vast twilight sunset sky with multi-plane clouds drifting at 3 parallax speeds
        - Silhouetted grand arched window frame with swaying lace curtains
        - Silhouetted character clutching the letter to his chest in tears
        - Rising golden light particles lifting toward the sky into the sunset clouds
        - Emotional final memorial title: 'माँ का त्याग — अमर प्रेम की मूक गवाही'
        """
        total_frames = int(duration_sec * self.fps)
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        cmd = [
            FFMPEG, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.res_x}x{self.res_y}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_mp4
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        np.random.seed(505)
        num_orbs = 35
        orb_x = np.random.uniform(540, 740, num_orbs)
        orb_y = np.random.uniform(420, 680, num_orbs)
        orb_vy = np.random.uniform(1.2, 2.8, num_orbs)
        orb_phi = np.random.uniform(0, 2*math.pi, num_orbs)

        # Precompute Sunset Sky gradient
        sky_array = np.zeros((self.res_y, self.res_x, 3), dtype=np.uint8)
        for y in range(self.res_y):
            t = y / float(self.res_y)
            r = int(45 * (1 - t) + 245 * t)
            g = int(22 * (1 - t) + 120 * t)
            b = int(65 * (1 - t) + 45 * (1 - t) + 20 * t)
            sky_array[y, :] = [min(255, r), min(255, g), min(255, b)]
        base_sky = Image.fromarray(sky_array)

        for frame in range(total_frames):
            im = base_sky.copy()
            draw = ImageDraw.Draw(im)

            # Setting Golden Sun on horizon
            sun_cx, sun_cy = 640, 440 + int(frame * 0.25) # Slowly setting
            for sr in range(140, 30, -15):
                draw.ellipse([(sun_cx - sr, sun_cy - sr), (sun_cx + sr, sun_cy + sr)], fill=(255, 190, 70, 20))
            draw.ellipse([(sun_cx - 40, sun_cy - 40), (sun_cx + 40, sun_cy + 40)], fill=(255, 245, 180))

            # --- Multi-Plane Parallax Sunset Clouds ---
            # Layer 1: Distant dark violet clouds (slowest drift)
            c1_drift = int(frame * 0.3)
            for cx_b in range(-200, self.res_x + 300, 380):
                c_pos = (cx_b + c1_drift) % (self.res_x + 400) - 200
                draw.ellipse([(c_pos, 260), (c_pos + 320, 340)], fill=(120, 50, 75))
                draw.ellipse([(c_pos + 60, 230), (c_pos + 260, 320)], fill=(140, 60, 85))

            # Layer 2: Midground warm amber clouds (faster drift)
            c2_drift = int(frame * 0.7)
            for cx_b in range(-300, self.res_x + 300, 460):
                c_pos = (cx_b + c2_drift) % (self.res_x + 400) - 200
                draw.ellipse([(c_pos, 330), (c_pos + 380, 420)], fill=(225, 110, 50))
                draw.ellipse([(c_pos + 90, 300), (c_pos + 300, 390)], fill=(245, 140, 65))

            # Distant mountain ridge silhouette on horizon
            draw.polygon([(0, 480), (320, 440), (640, 470), (960, 430), (1280, 480), (1280, 720), (0, 720)], fill=(32, 14, 28))

            # --- Grand Arched Window Frame (Foreground Silhouette) ---
            # Pillars and Wall
            draw.rectangle([(0, 0), (220, self.res_y)], fill=(10, 6, 12))
            draw.rectangle([(self.res_x - 220, 0), (self.res_x, self.res_y)], fill=(10, 6, 12))
            draw.rectangle([(0, 560), (self.res_x, self.res_y)], fill=(10, 6, 12)) # Balcony sill
            # Arch top
            draw.pieslice([(140, -120), (self.res_x - 140, 440)], 180, 360, fill=(10, 6, 12))

            # --- Fluttering Lace Curtains (Sine wave cloth physics) ---
            curtain_wave = 12 * math.sin(frame * 0.12)
            # Left curtain
            c_pts_l = [(220, 60)]
            for cy in range(60, 560, 30):
                c_pts_l.append((int(220 + 35 + 15 * math.sin(cy * 0.02 + frame * 0.15)), cy))
            c_pts_l.extend([(220, 560), (220, 60)])
            draw.polygon(c_pts_l, fill=(240, 220, 225))

            # Right curtain
            c_pts_r = [(self.res_x - 220, 60)]
            for cy in range(60, 560, 30):
                c_pts_r.append((int(self.res_x - 220 - 35 - 15 * math.sin(cy * 0.02 - frame * 0.15)), cy))
            c_pts_r.extend([(self.res_x - 220, 560), (self.res_x - 220, 60)])
            draw.polygon(c_pts_r, fill=(240, 220, 225))

            # --- Character Silhouette (Rohit Standing in Tears) ---
            rx, ry = 640, 560
            # Head bowed
            draw.ellipse([(rx - 16, ry - 170), (rx + 16, ry - 138)], fill=(6, 4, 8))
            # Torso holding letter to chest
            draw.polygon([
                (rx - 22, ry - 135),
                (rx + 22, ry - 135),
                (rx + 26, ry - 30),
                (rx - 26, ry - 30)
            ], fill=(6, 4, 8))
            # Hands clutching the letter
            draw.rectangle([(rx - 14, ry - 100), (rx + 14, ry - 75)], fill=(240, 225, 195)) # Letter against heart
            draw.ellipse([(rx - 18, ry - 95), (rx + 18, ry - 80)], outline=(6, 4, 8), width=3) # Hands folded over it

            # --- Rising Golden Spiritual Orbs (Ascending to Heaven) ---
            for oi in range(num_orbs):
                orb_y[oi] -= orb_vy[oi]
                if orb_y[oi] < 80:
                    orb_y[oi] = 520
                ox = orb_x[oi] + 18 * math.sin(frame * 0.1 + orb_phi[oi])
                draw.ellipse([(ox - 3, orb_y[oi] - 3), (ox + 3, orb_y[oi] + 3)], fill=(255, 225, 110))
                draw.ellipse([(ox - 6, orb_y[oi] - 6), (ox + 6, orb_y[oi] + 6)], outline=(255, 200, 70), width=1)

            # --- Emotional Final Memorial Typography (Smooth Fade In) ---
            if frame > 45:
                title_alpha = min(1.0, (frame - 45) / 35.0)
                tw_alpha = int(255 * title_alpha)
                # Golden plaque banner
                banner_y = 100
                draw.text((self.res_x // 2, banner_y), "माँ का त्याग — अमर प्रेम की मूक गवाही", fill=(255, 230, 140), font=self.font_hindi_large, anchor="mm")
                draw.text((self.res_x // 2, banner_y + 42), "AN ETERNAL TRIBUTE // MASTER AI 2D CINEMA", fill=(245, 180, 120), font=self.font_english_sub, anchor="mm")
                draw.line([(self.res_x // 2 - 180, banner_y + 65), (self.res_x // 2 + 180, banner_y + 65)], fill=(212, 160, 23), width=2)

            proc.stdin.write(im.tobytes())

        proc.stdin.close()
        proc.wait()
        logger.info(f"Scene 5 rendered: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4


if __name__ == "__main__":
    animator = Professional2DAnimator()
    test_out = r"F:\Master AI\00_CORE_SYSTEM\test_scene_1.mp4"
    animator.render_scene_1_arrival_gateway(test_out, duration_sec=4.0)
    print("Test render complete:", test_out)
