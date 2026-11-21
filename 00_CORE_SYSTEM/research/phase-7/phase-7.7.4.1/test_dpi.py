import fitz
from PIL import Image

svg = '<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg"><rect width="1920" height="1080" fill="#090508"/></svg>'
doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")

# Test dpi=72
pix72 = doc[0].get_pixmap(dpi=72)
print("pix72:", pix72.width, pix72.height, len(pix72.samples), len(pix72.samples) == 1920*1080*3)

# Test matrix=fitz.Matrix(1.0, 1.0)
pix_mat = doc[0].get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
print("pix_mat:", pix_mat.width, pix_mat.height, len(pix_mat.samples), len(pix_mat.samples) == 1920*1080*3)
