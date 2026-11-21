import bpy
import math
import os
import sys

def setup_benchmark_scene(res_x=1280, res_y=720, total_frames=120, samples=16, output_path=r"F:\Master AI\07_3D_CGI\renders\benchmark_720p\frame_"):
    # 1. Reset scene to factory empty state
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    
    # Render settings
    # Adaptive EEVEE engine selection (Blender 4.2 vs 5.2 LTS)
    if 'BLENDER_EEVEE_NEXT' in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys():
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.taa_render_samples = samples
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = output_path
    
    # 2. Ground Grid with subdivisions and material
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, y_subdivisions=20, size=30, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"
    
    mat_g = bpy.data.materials.new(name="GroundMat")
    mat_g.use_nodes = True
    nodes_g = mat_g.node_tree.nodes
    bsdf_g = nodes_g.get("Principled BSDF")
    bsdf_g.inputs['Base Color'].default_value = (0.2, 0.25, 0.22, 1.0) # Mossy earth
    bsdf_g.inputs['Roughness'].default_value = 0.85
    ground.data.materials.append(mat_g)
    
    # 3. Hero 3D Object (Hexagonal Beveled Monolith)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.6, depth=5.0, location=(0, 0, 2.5))
    monolith = bpy.context.active_object
    monolith.name = "HeroObject"
    
    # Bevel modifier
    bev = monolith.modifiers.new(name="Bevel", type='BEVEL')
    bev.width = 0.08
    bev.segments = 3
    
    mat_m = bpy.data.materials.new(name="MonoMat")
    mat_m.use_nodes = True
    nodes_m = mat_m.node_tree.nodes
    bsdf_m = nodes_m.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.08, 0.12, 0.18, 1.0) # Basalt
    bsdf_m.inputs['Metallic'].default_value = 0.4
    bsdf_m.inputs['Roughness'].default_value = 0.25
    monolith.data.materials.append(mat_m)
    
    # 4. Dynamic Lighting (Sun Key + Cool Fill)
    bpy.ops.object.light_add(type='SUN', location=(8, -8, 12))
    sun = bpy.context.active_object
    sun.data.energy = 4.5
    sun.data.color = (1.0, 0.95, 0.85) # Warm sunlight
    sun.data.angle = math.radians(1.5) # Soft shadows
    
    bpy.ops.object.light_add(type='POINT', location=(-6, 6, 4))
    fill = bpy.context.active_object
    fill.data.energy = 500.0
    fill.data.color = (0.3, 0.6, 1.0) # Cool blue fill
    
    # 5. Animated Camera Orbit
    bpy.ops.object.camera_add(location=(0, -8.5, 3.2))
    cam = bpy.context.active_object
    scene.camera = cam
    
    track = cam.constraints.new(type='TRACK_TO')
    track.target = monolith
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    for f in range(1, total_frames + 1):
        angle = math.radians((f / float(total_frames)) * 180.0 - 90.0)
        radius = 8.5
        cam.location.x = radius * math.sin(angle)
        cam.location.y = -radius * math.cos(angle)
        cam.location.z = 2.0 + 1.2 * math.sin(math.pi * f / float(total_frames))
        cam.keyframe_insert(data_path="location", frame=f)
    
    print("Benchmark scene setup completed successfully.")

if __name__ == "__main__":
    setup_benchmark_scene()
