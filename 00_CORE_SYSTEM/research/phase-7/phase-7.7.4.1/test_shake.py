import math, sys
sys.path.append(r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.7.4\engine")
from motion_director import Camera2D

cam = Camera2D()
for f in range(10):
    t = f / 24.0
    cam.trigger_shake(t, intensity=8.0)
    print(f"Frame {f:2d}: t={t:.4f}s -> shake_x={cam.shake_x:6.2f}, shake_y={cam.shake_y:6.2f}")
