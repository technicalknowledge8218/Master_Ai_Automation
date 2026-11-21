import os
from PIL import Image, ImageDraw

test_dir = r"F:\Master AI\00_CORE_SYSTEM\research\phase-7\oracle_cloud_reel\rig_test"
im = Image.open(os.path.join(test_dir, "arjun_head_sample.png")).convert("RGBA")
draw = ImageDraw.Draw(im)

# Mark potential eye coordinates (blue dots) and mouth (red box)
# Let's grid lines every 20px
for y in range(0, im.height, 20):
    draw.line([(0, y), (im.width, y)], fill=(100, 100, 100, 100), width=1)
    draw.text((2, y), str(y), fill=(255, 0, 0, 255))
for x in range(0, im.width, 20):
    draw.line([(x, 0), (x, im.height)], fill=(100, 100, 100, 100), width=1)
    draw.text((x, 2), str(x), fill=(0, 0, 255, 255))

im.save(os.path.join(test_dir, "arjun_head_grid.png"))

# Also Kabir
im_k = Image.open(os.path.join(test_dir, "dr_kabir_head_sample.png")).convert("RGBA")
draw_k = ImageDraw.Draw(im_k)
for y in range(0, im_k.height, 20):
    draw_k.line([(0, y), (im_k.width, y)], fill=(100, 100, 100, 100), width=1)
    draw_k.text((2, y), str(y), fill=(255, 0, 0, 255))
for x in range(0, im_k.width, 20):
    draw_k.line([(x, 0), (x, im_k.height)], fill=(100, 100, 100, 100), width=1)
    draw_k.text((x, 2), str(x), fill=(0, 0, 255, 255))

im_k.save(os.path.join(test_dir, "dr_kabir_head_grid.png"))
print("Saved head grids!")
