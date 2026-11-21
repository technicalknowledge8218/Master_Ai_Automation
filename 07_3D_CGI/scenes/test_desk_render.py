
import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24

world = bpy.data.worlds.new('DramaWorld')
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1.0)
    bg.inputs['Strength'].default_value = 0.2

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = 'Floor'

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 5, 5), rotation=(math.radians(90), 0, 0))
wall_back = bpy.context.active_object
wall_back.name = 'WallBack'

bpy.ops.mesh.primitive_plane_add(size=10, location=(-5, 0, 5), rotation=(0, math.radians(90), 0))
wall_left = bpy.context.active_object
wall_left.name = 'WallLeft'

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.4), scale=(2.2, 1.2, 0.1))
tabletop = bpy.context.active_object
tabletop.name = 'DeskTop'

for x, y in [(-0.95, -0.45), (0.95, -0.45), (-0.95, 0.45), (0.95, 0.45)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.35, location=(x, y, 0.675))

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1, 1.15), scale=(1.8, 0.9, 0.35))
drawer_unit = bpy.context.active_object

bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3, -0.1, 1.55), scale=(0.5, 0.35, 0.18))
letterbox = bpy.context.active_object
letterbox.name = 'LetterBox'

bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.3, -0.1, 1.46), rotation=(0, 0, math.radians(-15)), scale=(0.4, 0.3, 1.0))
parchment = bpy.context.active_object
parchment.name = 'AgedLetter'

bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.05, location=(-0.8, 0.3, 1.48))
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.45, location=(-0.8, 0.3, 1.7))
bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.18, location=(-0.8, 0.3, 1.95), rotation=(math.radians(180), 0, 0))

bpy.ops.object.light_add(type='POINT', location=(-0.8, 0.3, 1.85))
lamp_light = bpy.context.active_object
lamp_light.data.energy = 45.0
lamp_light.data.color = (1.0, 0.75, 0.45)

bpy.ops.object.light_add(type='SUN', location=(-4.0, -2.0, 4.0), rotation=(math.radians(45), math.radians(-25), math.radians(35)))
sun = bpy.context.active_object
sun.data.energy = 2.5
sun.data.color = (0.5, 0.65, 0.95)

bpy.ops.object.light_add(type='POINT', location=(1.5, -2.0, 2.5))
fill = bpy.context.active_object
fill.data.energy = 15.0
fill.data.color = (0.9, 0.85, 0.8)

bpy.ops.object.camera_add(location=(0, -3.2, 2.3), rotation=(math.radians(65), 0, 0))
cam = bpy.context.active_object
scene.camera = cam

scene.frame_start = 1
scene.frame_end = 24

scene.render.filepath = r'F:/Master AI/07_3D_CGI/renders/test_antique_desk_frame.png'
bpy.ops.render.render(write_still=True)
print('SUCCESS_RENDER_STILL')
