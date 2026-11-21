
import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24

world = bpy.data.worlds.new('DramaWorld')
scene.world = world

# Wooden desk surface
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 1.4))
mat_desk = bpy.data.materials.new(name='DeskMat')
bpy.context.active_object.data.materials.append(mat_desk)
if mat_desk.node_tree:
    bsdf = mat_desk.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.16, 0.08, 0.04, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.35

# Letter Box Base (dark mahogany & brass)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.0, 1.50), scale=(0.60, 0.42, 0.14))
box_base = bpy.context.active_object
mat_box = bpy.data.materials.new(name='BoxMat')
box_base.data.materials.append(mat_box)
if mat_box.node_tree:
    bsdf = mat_box.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.28, 0.18, 0.08, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.4
        bsdf.inputs['Roughness'].default_value = 0.25

# Brass hinges and lock
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.08, location=(0.0, -0.21, 1.50), rotation=(0, math.radians(90), 0))
mat_brass = bpy.data.materials.new(name='BrassMat')
bpy.context.active_object.data.materials.append(mat_brass)
if mat_brass.node_tree:
    bsdf = mat_brass.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.85, 0.68, 0.25, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.9
        bsdf.inputs['Roughness'].default_value = 0.2

# Aged letter envelope inside / next to box
bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.35, -0.05, 1.42), rotation=(0, 0, math.radians(-18)), scale=(0.40, 0.28, 1.0))
mat_env = bpy.data.materials.new(name='EnvMat')
bpy.context.active_object.data.materials.append(mat_env)
if mat_env.node_tree:
    bsdf = mat_env.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.80, 0.66, 1.0) # Yellowed vintage envelope
        bsdf.inputs['Roughness'].default_value = 0.8

# Warm desk lamp light nearby
bpy.ops.object.light_add(type='POINT', location=(-0.6, 0.4, 1.8))
lamp = bpy.context.active_object
lamp.data.energy = 50.0
lamp.data.color = (1.0, 0.75, 0.45)

# Soft moody fill light
bpy.ops.object.light_add(type='POINT', location=(0.8, -0.8, 1.9))
fill = bpy.context.active_object
fill.data.energy = 15.0
fill.data.color = (0.6, 0.7, 0.95)

# Camera: Macro angle focusing on box & envelope
bpy.ops.object.camera_add(location=(0.6, -0.7, 1.85), rotation=(math.radians(55), 0, math.radians(35)))
cam = bpy.context.active_object
scene.camera = cam

# Animate Camera slow pan & push
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (0.35, -0.52, 1.72)
cam.keyframe_insert(data_path='location', frame=24)

scene.frame_start = 1
scene.frame_end = 24

out_dir = r'F:/Master AI/07_3D_CGI/renders/test_box_anim'
os.makedirs(out_dir, exist_ok=True)
scene.render.filepath = os.path.join(out_dir, 'frame_')
scene.render.image_settings.file_format = 'PNG'

import time
t0 = time.time()
bpy.ops.render.render(animation=True)
t1 = time.time()
print(f'BOX_ANIM_DONE: 24 frames in {t1 - t0:.2f}s')
