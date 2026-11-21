"""
Master AI - Phase 7.2 Production Scene
Scene: African Savanna Establishing Environment (Sunrise Biome)
Integrates Poly Haven CC0 Aarfontein Sunrise HDRI & Aerial Ground Rock PBR Texture.
"""

import bpy
import math
import os

def build_savanna_establishing_scene(
    output_path=r"F:\Master AI\07_3D_CGI\renders\pilot_savanna_env\frame_",
    res_x=1280,
    res_y=720,
    total_frames=72,
    samples=16
):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # Dynamic Engine Selection (Blender 5.2 LTS vs 4.2 LTS)
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

    # ==========================================
    # 1. HDRI WORLD ENVIRONMENT LIGHTING
    # ==========================================
    hdri_path = r"F:\Master AI\15_ASSETS\open_source_library\hdri\aarfontein_sunrise_1k.hdr"
    world = bpy.data.worlds.new("SavannaWorld")
    scene.world = world
    world.use_nodes = True
    w_nodes = world.node_tree.nodes
    w_links = world.node_tree.links
    w_nodes.clear()

    node_bg = w_nodes.new(type='ShaderNodeBackground')
    node_out = w_nodes.new(type='ShaderNodeOutputWorld')
    node_bg.inputs['Strength'].default_value = 1.35
    w_links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

    if os.path.isfile(hdri_path):
        try:
            node_env = w_nodes.new(type='ShaderNodeTexEnvironment')
            node_env.image = bpy.data.images.load(hdri_path)
            w_links.new(node_env.outputs['Color'], node_bg.inputs['Color'])
            print(f"Loaded CC0 HDRI Environment: {hdri_path}")
        except Exception as e:
            print(f"Fallback world lighting: {e}")
            node_bg.inputs['Color'].default_value = (0.85, 0.65, 0.45, 1.0)
    else:
        node_bg.inputs['Color'].default_value = (0.85, 0.65, 0.45, 1.0)

    # ==========================================
    # 2. PBR TERRAIN WITH AERIAL GROUND ROCK TEXTURE
    # ==========================================
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=48, y_subdivisions=48, size=60, location=(0, 0, 0))
    terrain = bpy.context.active_object
    terrain.name = "SavannaGround"

    # Procedural gentle rolling terrain displacement
    disp = terrain.modifiers.new(name="TerrainRoll", type='DISPLACE')
    tex_noise = bpy.data.textures.new("TerrainNoise", type='CLOUDS')
    tex_noise.noise_scale = 3.5
    disp.texture = tex_noise
    disp.strength = 1.6

    mat_ground = bpy.data.materials.new(name="PBRSavannaGround")
    mat_ground.use_nodes = True
    g_nodes = mat_ground.node_tree.nodes
    g_links = mat_ground.node_tree.links
    bsdf_g = g_nodes.get("Principled BSDF")

    pbr_diff_path = r"F:\Master AI\15_ASSETS\open_source_library\textures\aerial_ground_rock_diff_1k.jpg"
    pbr_rough_path = r"F:\Master AI\15_ASSETS\open_source_library\textures\aerial_ground_rock_rough_1k.jpg"

    if os.path.isfile(pbr_diff_path):
        try:
            tex_img = g_nodes.new(type='ShaderNodeTexImage')
            tex_img.image = bpy.data.images.load(pbr_diff_path)
            
            # Texture coordinate & mapping for tiling
            tex_coord = g_nodes.new(type='ShaderNodeTexCoord')
            mapping = g_nodes.new(type='ShaderNodeMapping')
            mapping.inputs['Scale'].default_value = (8.0, 8.0, 8.0)
            
            g_links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
            g_links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])
            g_links.new(tex_img.outputs['Color'], bsdf_g.inputs['Base Color'])
            bsdf_g.inputs['Roughness'].default_value = 0.85
            print("Loaded PBR Ground Rock Texture Map")
        except Exception as e:
            print("Fallback procedural ground:", e)
            bsdf_g.inputs['Base Color'].default_value = (0.55, 0.42, 0.28, 1.0)
            bsdf_g.inputs['Roughness'].default_value = 0.90
    else:
        bsdf_g.inputs['Base Color'].default_value = (0.55, 0.42, 0.28, 1.0)
        bsdf_g.inputs['Roughness'].default_value = 0.90

    terrain.data.materials.append(mat_ground)

    # ==========================================
    # 3. ACACIA SAVANNA TREES & DISTANT HORIZONS
    # ==========================================
    mat_wood = bpy.data.materials.new(name="AcaciaBark")
    mat_wood.use_nodes = True
    mat_wood.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (0.22, 0.16, 0.12, 1.0)

    mat_canopy = bpy.data.materials.new(name="AcaciaCanopy")
    mat_canopy.use_nodes = True
    mat_canopy.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (0.28, 0.38, 0.15, 1.0)

    tree_positions = [
        (-8, 14, 0.2), (-14, 22, 0.5), (10, 18, 0.3), (16, 26, 0.6), (-3, 30, 0.8), (7, 36, 1.0)
    ]
    for idx, (tx, ty, tz) in enumerate(tree_positions):
        # Trunk
        bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=4.2, location=(tx, ty, tz + 2.1))
        trunk = bpy.context.active_object
        trunk.name = f"Trunk_{idx}"
        trunk.rotation_euler = (math.radians(-4 + idx * 2), math.radians(idx * 3), 0)
        trunk.data.materials.append(mat_wood)

        # Umbrella canopy
        bpy.ops.mesh.primitive_uv_sphere_add(radius=3.2, location=(tx, ty + 0.4, tz + 4.2))
        canopy = bpy.context.active_object
        canopy.name = f"Canopy_{idx}"
        canopy.scale = (1.4, 1.4, 0.32) # Flat umbrella shape
        canopy.data.materials.append(mat_canopy)

    # Distant Kopje Rock Formation
    bpy.ops.mesh.primitive_cube_add(size=12, location=(22, 42, 2.5))
    kopje = bpy.context.active_object
    kopje.name = "DistantKopje"
    kopje.scale = (1.8, 1.2, 0.6)
    kopje.rotation_euler = (math.radians(12), math.radians(24), math.radians(-30))
    kopje.data.materials.append(mat_ground)

    # ==========================================
    # 4. DIRECT SUNLIGHT RIG
    # ==========================================
    bpy.ops.object.light_add(type='SUN', location=(15, -20, 25))
    sun = bpy.context.active_object
    sun.data.energy = 5.8
    sun.data.color = (1.0, 0.92, 0.80) # Warm equatorial sun
    sun.data.angle = math.radians(10.0)
    sun.rotation_euler = (math.radians(55), math.radians(12), math.radians(-35))

    # ==========================================
    # 5. CINEMATIC GLIDING ESTABLISHING CAMERA
    # ==========================================
    bpy.ops.object.camera_add(location=(-6.0, -18.0, 5.5))
    cam = bpy.context.active_object
    scene.camera = cam

    # Focus target
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0.0, 16.0, 3.0))
    target = bpy.context.active_object
    target.name = "CamTarget"

    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Camera dolly trajectory across frames
    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        # Smooth forward tracking push
        cam.location.x = -6.0 + frac * 4.5
        cam.location.y = -18.0 + frac * 12.0
        cam.location.z = 5.5 - frac * 1.8
        cam.keyframe_insert(data_path="location", frame=f)

    print("Savanna Establishing Environment scene setup complete.")

if __name__ == "__main__":
    build_savanna_establishing_scene()
