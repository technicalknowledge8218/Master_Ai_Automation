
import bpy
import math
import time

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24

world = bpy.data.worlds.new('DramaWorld')
scene.world = world

# Desk & room
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.4), scale=(2.2, 1.2, 0.1))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.3, -0.1, 1.55), scale=(0.5, 0.35, 0.18))

# Light
bpy.ops.object.light_add(type='POINT', location=(-0.8, 0.3, 1.85))
lamp_light = bpy.context.active_object
lamp_light.data.energy = 45.0

# Camera
bpy.ops.object.camera_add(location=(0, -3.2, 2.3), rotation=(math.radians(65), 0, 0))
cam = bpy.context.active_object
scene.camera = cam

# Animate camera dolly
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (0, -2.2, 1.8)
cam.keyframe_insert(data_path='location', frame=24)

scene.frame_start = 1
scene.frame_end = 24

scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = r'F:/Master AI/07_3D_CGI/renders/bench_desk_anim.mp4'

t0 = time.time()
bpy.ops.render.render(animation=True)
t1 = time.time()
print(f'ANIM_RENDER_TIME: {t1 - t0:.2f}s for 24 frames ({24 / (t1 - t0):.2f} fps)')
