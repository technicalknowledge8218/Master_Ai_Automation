import fitz
svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff7e5f"/>
      <stop offset="100%" stop-color="#feb47b"/>
    </linearGradient>
  </defs>
  <rect width="400" height="400" fill="url(#grad)"/>
  <circle cx="200" cy="200" r="120" fill="#1e293b" stroke="#ffffff" stroke-width="6"/>
</svg>'''
doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
pix = doc[0].get_pixmap()
print("PyMuPDF SVG Pixmap:", pix.width, "x", pix.height, "Samples:", len(pix.samples))
