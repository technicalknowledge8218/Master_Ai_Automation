"""
Master AI - Phase 7.2 Production Scene
Scene: Hero African Lion atop Kopje overlooking Savanna (Cinematic 3D Character CGI)
Combines Anatomical Skeleton, PBR Subsurface Shading, Poly Haven CC0 HDRI & Ground PBR.
"""

import bpy
import math
import os

def build_lion_hero_scene(
    output_path=r"F:\Master AI\07_3D_CGI\renders\pilot_lion_hero\frame_",
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
    # 1. HDRI WORLD LIGHTING
    # ==========================================
    hdri_path = r"F:\Master AI\15_ASSETS\open_source_library\hdri\aarfontein_sunrise_1k.hdr"
    world = bpy.data.worlds.new("SavannaWorldLion")
    scene.world = world
    world.use_nodes = True
    w_nodes = world.node_tree.nodes
    w_links = world.node_tree.links
    w_nodes.clear()

    node_bg = w_nodes.new(type='ShaderNodeBackground')
    node_out = w_nodes.new(type='ShaderNodeOutputWorld')
    node_bg.inputs['Strength'].default_value = 1.25
    w_links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

    if os.path.isfile(hdri_path):
        try:
            node_env = w_nodes.new(type='ShaderNodeTexEnvironment')
            node_env.image = bpy.data.images.load(hdri_path)
            w_links.new(node_env.outputs['Color'], node_bg.inputs['Color'])
        except Exception:
            node_bg.inputs['Color'].default_value = (0.85, 0.65, 0.45, 1.0)
    else:
        node_bg.inputs['Color'].default_value = (0.85, 0.65, 0.45, 1.0)

    # ==========================================
    # 2. PBR ROCK KOPJE PEDESTAL
    # ==========================================
    bpy.ops.mesh.primitive_cube_add(size=4.5, location=(0, 0, 0.8))
    rock = bpy.context.active_object
    rock.name = "KopjeRock"
    rock.scale = (1.5, 1.2, 0.5)
    rock.rotation_euler = (math.radians(8), math.radians(-5), math.radians(15))

    mat_rock = bpy.data.materials.new(name="PBRKopje")
    mat_rock.use_nodes = True
    bsdf_r = mat_rock.node_tree.nodes.get("Principled BSDF")
    pbr_diff_path = r"F:\Master AI\15_ASSETS\open_source_library\textures\aerial_ground_rock_diff_1k.jpg"
    if os.path.isfile(pbr_diff_path):
        try:
            tex_img = mat_rock.node_tree.nodes.new(type='ShaderNodeTexImage')
            tex_img.image = bpy.data.images.load(pbr_diff_path)
            mat_rock.node_tree.links.new(tex_img.outputs['Color'], bsdf_r.inputs['Base Color'])
            bsdf_r.inputs['Roughness'].default_value = 0.82
        except Exception:
            bsdf_r.inputs['Base Color'].default_value = (0.45, 0.38, 0.30, 1.0)
    else:
        bsdf_r.inputs['Base Color'].default_value = (0.45, 0.38, 0.30, 1.0)
    rock.data.materials.append(mat_rock)

    # ==========================================
    # 3. ADVANCED ANATOMICAL LION MODEL & SHADERS
    # ==========================================
    # Golden Tawny Coat Material with SSS and Fur Bump
    mat_coat = bpy.data.materials.new(name="LionTawnyCoat")
    mat_coat.use_nodes = True
    bsdf_c = mat_coat.node_tree.nodes.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.76, 0.54, 0.28, 1.0)
    bsdf_c.inputs['Roughness'].default_value = 0.65
    bsdf_c.inputs['Subsurface Weight'].default_value = 0.22
    if 'Subsurface Radius' in bsdf_c.inputs:
        bsdf_c.inputs['Subsurface Radius'].default_value = (0.8, 0.4, 0.2)
    if 'Sheen Weight' in bsdf_c.inputs:
        bsdf_c.inputs['Sheen Weight'].default_value = 0.45

    tex_noise = mat_coat.node_tree.nodes.new(type='ShaderNodeTexNoise')
    tex_noise.inputs['Scale'].default_value = 45.0
    tex_noise.inputs['Detail'].default_value = 4.0
    bump_c = mat_coat.node_tree.nodes.new(type='ShaderNodeBump')
    bump_c.inputs['Strength'].default_value = 0.12
    mat_coat.node_tree.links.new(tex_noise.outputs['Fac'], bump_c.inputs['Height'])
    mat_coat.node_tree.links.new(bump_c.outputs['Normal'], bsdf_c.inputs['Normal'])

    # Dark Volumetric Mane Material
    mat_mane = bpy.data.materials.new(name="VolumetricManeDark")
    mat_mane.use_nodes = True
    bsdf_m = mat_mane.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.16, 0.10, 0.05, 1.0)
    bsdf_m.inputs['Roughness'].default_value = 0.85
    if 'Sheen Weight' in bsdf_m.inputs:
        bsdf_m.inputs['Sheen Weight'].default_value = 0.65

    # Black Leather (Nose, Lips, Eye Lining)
    mat_leather = bpy.data.materials.new(name="BlackLeatherNose")
    mat_leather.use_nodes = True
    bsdf_l = mat_leather.node_tree.nodes.get("Principled BSDF")
    bsdf_l.inputs['Base Color'].default_value = (0.04, 0.04, 0.04, 1.0)
    bsdf_l.inputs['Roughness'].default_value = 0.35

    # Amber Eyes
    mat_eye = bpy.data.materials.new(name="AmberLionEye")
    mat_eye.use_nodes = True
    bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")
    bsdf_e.inputs['Base Color'].default_value = (0.88, 0.58, 0.04, 1.0)
    bsdf_e.inputs['Roughness'].default_value = 0.05

    # --- Constructing Spine & Torso Hierarchy ---
    z_offset = 2.0 # Elevated on kopje rock
    
    # Thoracic Ribcage (Deep chest)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=1.0, location=(0, 0.45, z_offset + 1.25))
    chest = bpy.context.active_object
    chest.name = "LionChest"
    chest.scale = (1.18, 1.48, 1.28)
    chest.data.materials.append(mat_coat)

    # Lumbar Flank (Slender biological tuck)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.9, location=(0, -0.9, z_offset + 1.15))
    flank = bpy.context.active_object
    flank.name = "LionFlank"
    flank.scale = (0.85, 1.05, 0.95)
    flank.data.materials.append(mat_coat)

    # Pelvis / Haunches
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.95, location=(0, -1.95, z_offset + 1.20))
    haunches = bpy.context.active_object
    haunches.name = "LionHaunches"
    haunches.scale = (1.10, 1.25, 1.15)
    haunches.data.materials.append(mat_coat)

    # --- Neck & Cranial Structure ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.72, depth=1.35, location=(0, 1.45, z_offset + 1.70))
    neck = bpy.context.active_object
    neck.name = "LionNeck"
    neck.rotation_euler = (math.radians(-32), 0, 0)
    neck.scale = (1.1, 0.9, 1.2)
    neck.data.materials.append(mat_coat)

    # Cranium (Skull)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.75, location=(0, 2.05, z_offset + 2.35))
    cranium = bpy.context.active_object
    cranium.name = "LionCranium"
    cranium.scale = (0.88, 1.05, 0.92)
    cranium.data.materials.append(mat_coat)

    # Zygomatic Cheekbones
    for side in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.35, location=(side * 0.58, 2.15, z_offset + 2.25))
        cheek = bpy.context.active_object
        cheek.name = f"Cheek_{side}"
        cheek.scale = (0.5, 0.9, 0.7)
        cheek.data.materials.append(mat_coat)

    # Muzzle & Snout
    bpy.ops.mesh.primitive_cube_add(size=0.65, location=(0, 2.75, z_offset + 2.22))
    muzzle = bpy.context.active_object
    muzzle.name = "LionMuzzle"
    muzzle.scale = (0.88, 1.25, 0.72)
    muzzle.data.materials.append(mat_coat)

    # Black Nose Leather
    bpy.ops.mesh.primitive_cube_add(size=0.25, location=(0, 3.16, z_offset + 2.38))
    nose = bpy.context.active_object
    nose.name = "LionNose"
    nose.scale = (1.0, 0.5, 0.6)
    nose.data.materials.append(mat_leather)

    # Amber Eyes with Depth
    for side in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.12, location=(side * 0.38, 2.60, z_offset + 2.50))
        eye = bpy.context.active_object
        eye.name = f"Eye_{side}"
        eye.data.materials.append(mat_eye)

    # Rounded Feline Ears
    for side in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.28, location=(side * 0.72, 1.95, z_offset + 2.85))
        ear = bpy.context.active_object
        ear.name = f"Ear_{side}"
        ear.scale = (0.35, 0.75, 0.95)
        ear.rotation_euler = (math.radians(-15), side * math.radians(25), side * math.radians(-20))
        ear.data.materials.append(mat_coat)

    # --- 3-Tier Volumetric Mane Shells ---
    mane_specs = [
        ("ManeInner", 1.25, (0, 1.55, z_offset + 2.05), (1.35, 1.20, 1.35)),
        ("ManeMiddle", 1.45, (0, 1.25, z_offset + 1.85), (1.50, 1.35, 1.40)),
        ("ManeOuter", 1.65, (0, 0.95, z_offset + 1.65), (1.60, 1.45, 1.45))
    ]
    for mname, mrad, mloc, mscale in mane_specs:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=mrad, location=mloc)
        mshell = bpy.context.active_object
        mshell.name = mname
        mshell.scale = mscale
        # Noise displacement on mane shells for organic silhouette
        disp_m = mshell.modifiers.new(name="ManeDisplace", type='DISPLACE')
        tex_m = bpy.data.textures.new(f"Tex_{mname}", type='CLOUDS')
        tex_m.noise_scale = 1.2
        disp_m.texture = tex_m
        disp_m.strength = 0.22
        mshell.data.materials.append(mat_mane)

    # --- Digitigrade Legs and Paws ---
    leg_coords = [
        ("ForeL", -0.75, 0.85, z_offset + 0.65, 1.35),
        ("ForeR",  0.75, 0.85, z_offset + 0.65, 1.35),
        ("HindL", -0.82, -1.85, z_offset + 0.60, 1.30),
        ("HindR",  0.82, -1.85, z_offset + 0.60, 1.30)
    ]
    for lname, lx, ly, lz, lheight in leg_coords:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=lheight, location=(lx, ly, lz))
        leg = bpy.context.active_object
        leg.name = lname
        leg.data.materials.append(mat_coat)

        # Paw Pad
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.28, location=(lx, ly + 0.12, lz - lheight/2.0 + 0.12))
        paw = bpy.context.active_object
        paw.name = f"Paw_{lname}"
        paw.scale = (1.1, 1.4, 0.55)
        paw.data.materials.append(mat_coat)

    # --- Tail with Tassel ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.75, location=(0, -2.95, z_offset + 0.65))
    tail = bpy.context.active_object
    tail.name = "LionTail"
    tail.rotation_euler = (math.radians(-48), 0, 0)
    tail.data.materials.append(mat_coat)

    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.18, location=(0, -3.65, z_offset + 0.05))
    tassel = bpy.context.active_object
    tassel.name = "LionTassel"
    tassel.data.materials.append(mat_mane)

    # ==========================================
    # 4. LIGHTING RIG
    # ==========================================
    bpy.ops.object.light_add(type='SUN', location=(10, -15, 20))
    sun = bpy.context.active_object
    sun.data.energy = 5.5
    sun.data.color = (1.0, 0.92, 0.78)
    sun.rotation_euler = (math.radians(52), math.radians(10), math.radians(-30))

    # Rim Backlight for Mane Separation
    bpy.ops.object.light_add(type='SPOT', location=(-4.5, -6.5, z_offset + 4.5))
    rim = bpy.context.active_object
    rim.data.energy = 950.0
    rim.data.color = (0.35, 0.65, 1.0)
    rim.rotation_euler = (math.radians(110), math.radians(-25), math.radians(45))

    # ==========================================
    # 5. PROCEDURAL KEYFRAMING & HERO ORBITAL CAMERA
    # ==========================================
    bpy.ops.object.camera_add(location=(0, 7.5, z_offset + 2.5))
    cam = bpy.context.active_object
    scene.camera = cam

    track = cam.constraints.new(type='TRACK_TO')
    track.target = cranium
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        # Respiratory rise/fall
        chest_scale_z = 1.28 + 0.04 * math.sin(f * 0.22)
        chest.scale.z = chest_scale_z
        chest.keyframe_insert(data_path="scale", frame=f)

        # Subtle head look-at vigilance
        cranium.rotation_euler.z = math.radians(6 * math.sin(f * 0.15))
        cranium.keyframe_insert(data_path="rotation_euler", frame=f)

        # Tail swish
        tail.rotation_euler.y = math.radians(10 * math.sin(f * 0.25))
        tail.keyframe_insert(data_path="rotation_euler", frame=f)

        # Heroic low-to-mid angle orbital arc
        angle = math.radians(frac * 75.0 - 37.5)
        radius = 6.8
        cam.location.x = radius * math.sin(angle)
        cam.location.y = 1.0 + radius * math.cos(angle)
        cam.location.z = z_offset + 2.4 - 0.7 * math.sin(frac * math.pi)
        cam.keyframe_insert(data_path="location", frame=f)

    print("Hero Lion CGI scene setup complete.")

if __name__ == "__main__":
    build_lion_hero_scene()
