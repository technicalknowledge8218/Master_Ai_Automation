import os

files = [
    r"F:\Master AI\07_3D_CGI\scenes\scene_benchmark.py",
    r"F:\Master AI\07_3D_CGI\scenes\scene_nature_environment.py",
    r"F:\Master AI\07_3D_CGI\scenes\scene_animal_cgi.py",
    r"F:\Master AI\07_3D_CGI\scenes\scene_scientific_viz.py"
]

pattern = "scene.render.engine = 'BLENDER_EEVEE_NEXT'"
replacement = """# Adaptive EEVEE engine selection (Blender 4.2 vs 5.2 LTS)
    if 'BLENDER_EEVEE_NEXT' in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys():
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'"""

for f in files:
    with open(f, 'r') as fp:
        content = fp.read()
    if pattern in content:
        content = content.replace(pattern, replacement)
        with open(f, 'w') as fp:
            fp.write(content)
        print(f"Updated {os.path.basename(f)} for adaptive Blender 4.2/5.2 support.")
    else:
        print(f"Pattern not found in {os.path.basename(f)} (already updated or different).")
