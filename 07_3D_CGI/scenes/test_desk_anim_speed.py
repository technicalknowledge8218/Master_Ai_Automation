
import bpy
import math
import os
import sys

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24

world = bpy.data.worlds.new('DramaWorld')
scene.world = world

# Dark moody room environment
# Floor with dark wood tone
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
floor = bpy.context.active_object
mat_floor = bpy.data.materials.new(name='FloorMat')
floor.data.materials.append(mat_floor)
if mat_floor.node_tree:
    bsdf = mat_floor.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.08, 0.05, 0.03, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.6

# Back Wall
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 6, 6), rotation=(math.radians(90), 0, 0))
wall_back = bpy.context.active_object
mat_wall = bpy.data.materials.new(name='WallMat')
wall_back.data.materials.append(mat_wall)
if mat_wall.node_tree:
    bsdf = mat_wall.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)

# Left Wall with Window Cutout
bpy.ops.mesh.primitive_plane_add(size=12, location=(-6, 0, 6), rotation=(0, math.radians(90), 0))
wall_left = bpy.context.active_object
wall_left.data.materials.append(mat_wall)

# Antique Wooden Writing Desk
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.4), scale=(2.4, 1.3, 0.12))
desk = bpy.context.active_object
mat_desk = bpy.data.materials.new(name='DeskMat')
desk.data.materials.append(mat_desk)
if mat_desk.node_tree:
    bsdf = mat_desk.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.15, 0.08, 0.04, 1.0) # Mahogany
        bsdf.inputs['Roughness'].default_value = 0.4

# Desk Legs
for lx, ly in [(-1.05, -0.5), (1.05, -0.5), (-1.05, 0.5), (1.05, 0.5)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.34, location=(lx, ly, 0.67))
    bpy.context.active_object.data.materials.append(mat_desk)

# Drawer Pedestal
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1, 1.12), scale=(2.0, 1.0, 0.38))
drawer = bpy.context.active_object
drawer.data.materials.append(mat_desk)

# Antique Ornate Keepsake Letter Box (Brass & Dark Walnut)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.35, -0.15, 1.56), scale=(0.55, 0.38, 0.16))
box = bpy.context.active_object
mat_box = bpy.data.materials.new(name='BoxMat')
box.data.materials.append(mat_box)
if mat_box.node_tree:
    bsdf = mat_box.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.35, 0.25, 0.10, 1.0) # Brass/Walnut
        bsdf.inputs['Metallic'].default_value = 0.6
        bsdf.inputs['Roughness'].default_value = 0.3

# Aged Parchment Letter on Desk
bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.35, -0.12, 1.47), rotation=(0, 0, math.radians(-12)), scale=(0.42, 0.32, 1.0))
parchment = bpy.context.active_object
mat_paper = bpy.data.materials.new(name='PaperMat')
parchment.data.materials.append(mat_paper)
if mat_paper.node_tree:
    bsdf = mat_paper.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.85, 0.78, 0.65, 1.0) # Aged yellowed paper
        bsdf.inputs['Roughness'].default_value = 0.85

# Vintage Brass Desk Lamp
bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.06, location=(-0.85, 0.35, 1.49))
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.48, location=(-0.85, 0.35, 1.73))
bpy.ops.mesh.primitive_cone_add(radius1=0.22, depth=0.20, location=(-0.85, 0.35, 1.98), rotation=(math.radians(180), 0, 0))

# Lights
# Warm point lamp light
bpy.ops.object.light_add(type='POINT', location=(-0.85, 0.35, 1.88))
lamp_light = bpy.context.active_object
lamp_light.data.energy = 55.0
lamp_light.data.color = (1.0, 0.72, 0.40)

# Window Dusk Sun light beam
bpy.ops.object.light_add(type='SUN', location=(-5.0, -3.0, 5.0), rotation=(math.radians(48), math.radians(-30), math.radians(40)))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.data.color = (0.55, 0.65, 0.95)

# Soft Fill light
bpy.ops.object.light_add(type='POINT', location=(2.0, -2.5, 3.0))
fill = bpy.context.active_object
fill.data.energy = 18.0
fill.data.color = (0.85, 0.82, 0.80)

# Camera
bpy.ops.object.camera_add(location=(0, -3.4, 2.4), rotation=(math.radians(64), 0, 0))
cam = bpy.context.active_object
scene.camera = cam

# Set frame range for test (frames 1 to 24)
scene.frame_start = 1
scene.frame_end = 24

# Animate Camera Dolly In
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (0, -2.2, 1.8)
cam.keyframe_insert(data_path='location', frame=24)

# Setup output
out_dir = r'F:/Master AI/07_3D_CGI/renders/test_desk_anim'
os.makedirs(out_dir, exist_ok=True)
scene.render.filepath = os.path.join(out_dir, 'frame_')
scene.render.image_settings.file_format = 'PNG'

import time
t0 = time.time()
bpy.ops.render.render(animation=True)
t1 = time.time()
print(f'RENDER_DONE: 24 frames in {t1 - t0:.2f}s ({24 / (t1 - t0):.2f} fps)')
