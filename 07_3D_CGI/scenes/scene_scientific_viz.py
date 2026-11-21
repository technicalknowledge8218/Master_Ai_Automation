import bpy
import math

def build_scientific_visualization(
    output_path=r"F:\Master AI\07_3D_CGI\renders\scientific_viz\frame_",
    res_x=1280,
    res_y=720,
    total_frames=120,
    samples=16
):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    
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
    scene.render.filepath = output_path
    
    # 1. Measurement Grid Ground
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=30, y_subdivisions=30, size=24, location=(0, 0, -3.0))
    grid = bpy.context.active_object
    mat_grid = bpy.data.materials.new(name="SciGrid")
    mat_grid.use_nodes = True
    bg = mat_grid.node_tree.nodes.get("Principled BSDF")
    bg.inputs['Base Color'].default_value = (0.05, 0.08, 0.12, 1.0)
    bg.inputs['Roughness'].default_value = 0.4
    grid.data.materials.append(mat_grid)
    
    # Materials for Scientific Model
    mat_core = bpy.data.materials.new(name="CoreMat")
    mat_core.use_nodes = True
    bc = mat_core.node_tree.nodes.get("Principled BSDF")
    bc.inputs['Base Color'].default_value = (0.9, 0.25, 0.15, 1.0)
    bc.inputs['Metallic'].default_value = 0.8
    bc.inputs['Roughness'].default_value = 0.2
    
    mat_ring = bpy.data.materials.new(name="OrbitalRingMat")
    mat_ring.use_nodes = True
    br = mat_ring.node_tree.nodes.get("Principled BSDF")
    br.inputs['Base Color'].default_value = (0.1, 0.7, 0.9, 1.0)
    br.inputs['Metallic'].default_value = 0.9
    br.inputs['Roughness'].default_value = 0.1
    
    mat_glow = bpy.data.materials.new(name="GlowMat")
    mat_glow.use_nodes = True
    nodes_glow = mat_glow.node_tree.nodes
    nodes_glow.clear()
    out_node = nodes_glow.new(type='ShaderNodeOutputMaterial')
    emit_node = nodes_glow.new(type='ShaderNodeEmission')
    emit_node.inputs['Color'].default_value = (0.2, 0.8, 1.0, 1.0) # Electric cyan
    emit_node.inputs['Strength'].default_value = 8.0
    mat_glow.node_tree.links.new(emit_node.outputs['Emission'], out_node.inputs['Surface'])
    
    # 2. Central Molecular / Atomic Nucleus
    nucleus_group = []
    core_offsets = [(0, 0, 0), (0.7, 0.4, 0.3), (-0.6, -0.5, 0.4), (0.3, -0.6, -0.5), (-0.4, 0.7, -0.3)]
    for cx, cy, cz in core_offsets:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(cx, cy, cz))
        part = bpy.context.active_object
        part.data.materials.append(mat_core)
        nucleus_group.append(part)
        
    # 3. Gimbal Orbital Rings (Torus)
    rings = []
    ring_configs = [(3.2, 0.06, (45, 0, 0)), (3.8, 0.06, (0, 60, 45)), (4.4, 0.06, (-45, 30, 0))]
    for r_maj, r_min, rot in ring_configs:
        bpy.ops.mesh.primitive_torus_add(major_radius=r_maj, minor_radius=r_min, location=(0, 0, 0))
        torus = bpy.context.active_object
        torus.rotation_euler = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))
        torus.data.materials.append(mat_ring)
        rings.append((torus, rot))
        
        # Add glowing orbital node on each ring
        node_angle = math.radians(rot[2])
        nx = r_maj * math.cos(node_angle)
        ny = r_maj * math.sin(node_angle)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(nx, ny, 0))
        node_sphere = bpy.context.active_object
        node_sphere.data.materials.append(mat_glow)
        
    # 4. Animated Rotation over timeline
    for f in range(1, total_frames + 1):
        deg = (f / float(total_frames)) * 360.0
        # Rotate rings
        for idx, (rng, base_rot) in enumerate(rings):
            factor = (idx + 1) * 1.5
            rng.rotation_euler.z = math.radians(base_rot[2] + deg * factor)
            rng.keyframe_insert(data_path="rotation_euler", frame=f)
            
    # 5. Scientific Lighting (High-Contrast Specular)
    bpy.ops.object.light_add(type='POINT', location=(6, -6, 8))
    key = bpy.context.active_object
    key.data.energy = 800.0
    key.data.color = (1.0, 1.0, 1.0)
    
    bpy.ops.object.light_add(type='POINT', location=(-6, 6, -2))
    rim = bpy.context.active_object
    rim.data.energy = 500.0
    rim.data.color = (0.2, 0.6, 1.0)
    
    # 6. Camera Elevation & Spiral
    bpy.ops.object.camera_add(location=(0, -9.5, 4.0))
    cam = bpy.context.active_object
    scene.camera = cam
    
    track = cam.constraints.new(type='TRACK_TO')
    track.target = nucleus_group[0]
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        cam_angle = math.radians(frac * 180.0 - 90.0)
        dist = 8.5
        cam.location.x = dist * math.sin(cam_angle)
        cam.location.y = -dist * math.cos(cam_angle)
        cam.location.z = 2.0 + 3.5 * math.sin(frac * math.pi)
        cam.keyframe_insert(data_path="location", frame=f)

if __name__ == "__main__":
    build_scientific_visualization()
