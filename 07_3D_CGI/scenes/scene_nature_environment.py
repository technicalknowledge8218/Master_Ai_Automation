import bpy
import math
import random

def build_nature_environment(
    output_path=r"F:\Master AI\07_3D_CGI\renders\nature_env\frame_",
    res_x=1280,
    res_y=720,
    total_frames=120,
    samples=16
):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    
    # Engine Settings
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
    
    # 1. Rolling Savanna Terrain
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=40, size=50, location=(0, 0, 0))
    terrain = bpy.context.active_object
    terrain.name = "SavannaTerrain"
    
    # Apply vertex displacement for hills
    mesh = terrain.data
    for v in mesh.vertices:
        x, y = v.co.x, v.co.y
        # Procedural rolling dune/hill height
        v.co.z = 0.8 * math.sin(x * 0.15) * math.cos(y * 0.12) + 0.3 * math.sin(x * 0.4 + y * 0.3)
    mesh.update()
    
    # Terrain Material
    mat_t = bpy.data.materials.new(name="SavannaGround")
    mat_t.use_nodes = True
    bsdf_t = mat_t.node_tree.nodes.get("Principled BSDF")
    bsdf_t.inputs['Base Color'].default_value = (0.58, 0.48, 0.32, 1.0) # Golden dry earth
    bsdf_t.inputs['Roughness'].default_value = 0.9
    terrain.data.materials.append(mat_t)
    
    # 2. Procedural Acacia Trees
    def create_acacia_tree(x_pos, y_pos, z_pos, scale=1.0):
        # Trunk
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.25 * scale, depth=3.5 * scale, location=(x_pos, y_pos, z_pos + 1.75 * scale))
        trunk = bpy.context.active_object
        trunk.rotation_euler = (math.radians(random.uniform(-5, 5)), math.radians(random.uniform(-5, 5)), 0)
        
        mat_wood = bpy.data.materials.get("AcaciaWood")
        if not mat_wood:
            mat_wood = bpy.data.materials.new(name="AcaciaWood")
            mat_wood.use_nodes = True
            b = mat_wood.node_tree.nodes.get("Principled BSDF")
            b.inputs['Base Color'].default_value = (0.22, 0.16, 0.11, 1.0)
            b.inputs['Roughness'].default_value = 0.85
        trunk.data.materials.append(mat_wood)
        
        # Umbrella Canopy
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=2.5 * scale, depth=0.4 * scale, location=(x_pos, y_pos, z_pos + 3.6 * scale))
        canopy = bpy.context.active_object
        
        mat_leaf = bpy.data.materials.get("AcaciaLeaf")
        if not mat_leaf:
            mat_leaf = bpy.data.materials.new(name="AcaciaLeaf")
            mat_leaf.use_nodes = True
            b = mat_leaf.node_tree.nodes.get("Principled BSDF")
            b.inputs['Base Color'].default_value = (0.28, 0.38, 0.18, 1.0) # Olive savanna foliage
            b.inputs['Roughness'].default_value = 0.6
        canopy.data.materials.append(mat_leaf)

    random.seed(42)
    tree_coords = [(-8, 5), (6, 8), (-4, -6), (10, -4), (-12, 12), (14, 14)]
    for tx, ty in tree_coords:
        create_acacia_tree(tx, ty, 0, scale=random.uniform(0.9, 1.3))

    # 3. Atmospheric Golden Hour Lighting
    bpy.ops.object.light_add(type='SUN', location=(20, -25, 8))
    sun = bpy.context.active_object
    sun.data.energy = 5.5
    sun.data.color = (1.0, 0.82, 0.60) # Golden hour warm sunlight
    sun.data.angle = math.radians(2.0) # Soft shadow edge
    
    # Ambient Sky Fill
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 15))
    fill = bpy.context.active_object
    fill.data.energy = 800.0
    fill.data.color = (0.45, 0.65, 0.90) # Cool blue sky dome fill

    # 4. Animated Camera Dolly Track
    bpy.ops.object.camera_add(location=(-15, -18, 4.5))
    cam = bpy.context.active_object
    scene.camera = cam
    
    # Animate Dolly forward through landscape
    cam.rotation_euler = (math.radians(82), 0, math.radians(-40))
    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        cam.location.x = -15.0 + 12.0 * frac
        cam.location.y = -18.0 + 14.0 * frac
        cam.location.z = 4.2 + 0.5 * math.sin(frac * math.pi)
        cam.keyframe_insert(data_path="location", frame=f)

if __name__ == "__main__":
    build_nature_environment()
