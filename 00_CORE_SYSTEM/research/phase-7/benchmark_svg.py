import time
import pymupdf

svg_test = '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a1128"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#bg)"/>
  <circle cx="960" cy="540" r="300" fill="#f59e0b" stroke="#ffffff" stroke-width="10"/>
</svg>'''

t0 = time.time()
doc = pymupdf.open(stream=svg_test.encode("utf-8"), filetype="svg")
pix = doc[0].get_pixmap()
dt = time.time() - t0
print(f"1080p SVG Rasterization Time: {dt*1000:.2f} ms | Size: {pix.width}x{pix.height} | Bytes: {len(pix.samples)}")
