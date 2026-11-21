"""
Master AI - 3D CGI Production Module
Scene: Advanced Improved Feline CGI Prototype (African Lion)
"""

import bpy
import math

def build_improved_lion_scene(
    output_path=r"F:\Master AI\07_3D_CGI\renders\improved_lion\frame_",
    res_x=1280,
    res_y=720,
    total_frames=72,
    samples=16
):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    
    # Adaptive Engine Selection (Blender 5.2 vs 4.2 LTS)
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
    # 1. SHADERS & MATERIALS (PBR + SSS + FUR GRAIN)
    # ==========================================
    # Tawny Feline Coat
    mat_coat = bpy.data.materials.new(name="AdvancedCoat")
    mat_coat.use_nodes = True
    nodes_c = mat_coat.node_tree.nodes
    bsdf_c = nodes_c.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.76, 0.54, 0.28, 1.0) # Golden savannah coat
    bsdf_c.inputs['Roughness'].default_value = 0.65
    bsdf_c.inputs['Subsurface Weight'].default_value = 0.22 # Organic flesh/fur scatter
    if 'Subsurface Radius' in bsdf_c.inputs:
        bsdf_c.inputs['Subsurface Radius'].default_value = (0.8, 0.4, 0.2) # Warm subcutaneous tint
    if 'Sheen Weight' in bsdf_c.inputs:
        bsdf_c.inputs['Sheen Weight'].default_value = 0.4 # Fur rim sheen

    # Procedural Fur Grain Bump
    tex_noise = nodes_c.new(type='ShaderNodeTexNoise')
    tex_noise.inputs['Scale'].default_value = 45.0
    tex_noise.inputs['Detail'].default_value = 4.0
    bump_c = nodes_c.new(type='ShaderNodeBump')
    bump_c.inputs['Strength'].default_value = 0.12
    mat_coat.node_tree.links.new(tex_noise.outputs['Fac'], bump_c.inputs['Height'])
    mat_coat.node_tree.links.new(bump_c.outputs['Normal'], bsdf_c.inputs['Normal'])

    # Dark Mane Material
    mat_mane = bpy.data.materials.new(name="VolumetricMane")
    mat_mane.use_nodes = True
    bsdf_m = mat_mane.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.18, 0.11, 0.06, 1.0) # Deep charcoal brown mane
    bsdf_m.inputs['Roughness'].default_value = 0.85
    if 'Sheen Weight' in bsdf_m.inputs:
        bsdf_m.inputs['Sheen Weight'].default_value = 0.6

    # Black Leather (Nose, Lips, Eye Lining)
    mat_leather = bpy.data.materials.new(name="BlackLeather")
    mat_leather.use_nodes = True
    bsdf_l = mat_leather.node_tree.nodes.get("Principled BSDF")
    bsdf_l.inputs['Base Color'].default_value = (0.04, 0.04, 0.04, 1.0)
    bsdf_l.inputs['Roughness'].default_value = 0.35 # Wet nose leather specular

    # Amber Eyes
    mat_eye = bpy.data.materials.new(name="AmberEye")
    mat_eye.use_nodes = True
    bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")
    bsdf_e.inputs['Base Color'].default_value = (0.85, 0.55, 0.05, 1.0)
    bsdf_e.inputs['Roughness'].default_value = 0.05 # Glossy cornea

    # ==========================================
    # 2. GROUND SAVANNA ROCK PEDESTAL
    # ==========================================
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=6.5, depth=0.8, location=(0, 0, -0.4))
    pedestal = bpy.context.active_object
    pedestal.name = "RockyPedestal"
    mat_rock = bpy.data.materials.new(name="PedestalRock")
    mat_rock.use_nodes = True
    bsdf_r = mat_rock.node_tree.nodes.get("Principled BSDF")
    bsdf_r.inputs['Base Color'].default_value = (0.32, 0.28, 0.23, 1.0)
    bsdf_r.inputs['Roughness'].default_value = 0.92
    pedestal.data.materials.append(mat_rock)

    # ==========================================
    # 3. ANATOMICAL LION GEOMETRY
    # ==========================================
    # A. Thoracic Spine & Ribcage
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.25, location=(0, 0.8, 2.3))
    chest = bpy.context.active_object
    chest.name = "LionChest"
    chest.scale = (0.95, 1.25, 1.15) # Deep pectoral mass
    chest.data.materials.append(mat_coat)

    # B. Lumbar / Tucked Abdomen
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.05, location=(0, -0.4, 2.2))
    belly = bpy.context.active_object
    belly.scale = (0.82, 1.1, 0.95) # Narrow flank
    belly.data.materials.append(mat_coat)

    # C. Pelvis / Haunches
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.1, location=(0, -1.6, 2.1))
    pelvis = bpy.context.active_object
    pelvis.scale = (0.9, 1.15, 1.1)
    pelvis.data.materials.append(mat_coat)

    # D. Four Articulated Limbs with Hock & Paws
    limb_specs = [
        ("FrontLeft", -0.75, 1.0, 1.2, 0.26, 2.2, 0.15),
        ("FrontRight", 0.75, 1.0, 1.2, 0.26, 2.2, 0.15),
        ("BackLeft", -0.80, -1.6, 1.1, 0.28, 2.0, -0.2),
        ("BackRight", 0.80, -1.6, 1.1, 0.28, 2.0, -0.2)
    ]
    for name, lx, ly, lz, rad, depth, forward_ang in limb_specs:
        # Upper Leg
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=rad, depth=depth, location=(lx, ly, lz))
        leg = bpy.context.active_object
        leg.name = f"Leg_{name}"
        leg.rotation_euler = (math.radians(forward_ang * 15), 0, 0)
        leg.data.materials.append(mat_coat)

        # Paw (Broad pad with 4 digital toes)
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=rad * 1.5, depth=0.25, location=(lx, ly + 0.15, 0.12))
        paw = bpy.context.active_object
        paw.name = f"Paw_{name}"
        paw.data.materials.append(mat_coat)

    # E. Neck & Cervical Mass
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.75, depth=1.6, location=(0, 1.9, 2.7))
    neck = bpy.context.active_object
    neck.rotation_euler = (math.radians(45), 0, 0)
    neck.data.materials.append(mat_coat)

    # F. Multi-Tier Volumetric Mane Clustered Shells
    # Layer 1: Shoulder cape
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.65, location=(0, 1.1, 2.5))
    m1 = bpy.context.active_object
    m1.scale = (0.95, 0.9, 1.15)
    m1.data.materials.append(mat_mane)

    # Layer 2: Cervical collar
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.55, location=(0, 1.7, 2.8))
    m2 = bpy.context.active_object
    m2.scale = (0.92, 0.85, 1.1)
    m2.data.materials.append(mat_mane)

    # Layer 3: Throat bib / brisket
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.35, location=(0, 2.1, 2.4))
    m3 = bpy.context.active_object
    m3.scale = (0.8, 0.7, 1.3)
    m3.data.materials.append(mat_mane)

    # G. Detailed Feline Head & Facial Architecture
    # Cranium (Broad forehead)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.72, location=(0, 2.6, 3.1))
    cranium = bpy.context.active_object
    cranium.name = "LionCranium"
    cranium.scale = (1.05, 1.0, 0.95)
    cranium.data.materials.append(mat_coat)

    # Zygomatic Cheek Fluff
    for sx in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.38, location=(sx, 2.6, 2.9))
        cheek = bpy.context.active_object
        cheek.scale = (1.1, 0.8, 0.8)
        cheek.data.materials.append(mat_mane)

    # Muzzle & Whisker Pads (Broad feline snout)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.40, depth=0.85, location=(0, 3.15, 2.85))
    muzzle = bpy.context.active_object
    muzzle.rotation_euler = (math.radians(82), 0, 0)
    muzzle.scale = (1.1, 1.0, 0.85)
    muzzle.data.materials.append(mat_coat)

    # Black Nose Leather
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=0.15, location=(0, 3.55, 2.95))
    nose = bpy.context.active_object
    nose.rotation_euler = (math.radians(90), 0, 0)
    nose.data.materials.append(mat_leather)

    # Lower Jaw (Chin)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=0.6, location=(0, 3.05, 2.62))
    chin = bpy.context.active_object
    chin.rotation_euler = (math.radians(82), 0, 0)
    chin.data.materials.append(mat_coat)

    # Amber Eyes with dark orbital margins
    for ex in [-0.32, 0.32]:
        # Eye socket margin
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(ex, 3.05, 3.18))
        socket = bpy.context.active_object
        socket.data.materials.append(mat_leather)
        # Eyeball
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(ex, 3.08, 3.19))
        eye = bpy.context.active_object
        eye.data.materials.append(mat_eye)

    # Rounded Feline Ears with pale interior
    for ex in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=0.1, location=(ex, 2.45, 3.65))
        ear = bpy.context.active_object
        ear.rotation_euler = (math.radians(40), math.radians(ex * 35), 0)
        ear.data.materials.append(mat_coat)

    # H. Tufted Tail
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.10, depth=2.4, location=(0, -2.7, 1.6))
    tail = bpy.context.active_object
    tail.rotation_euler = (math.radians(-35), 0, 0)
    tail.data.materials.append(mat_coat)

    # Tail Tuft
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.24, location=(0, -3.4, 0.8))
    tuft = bpy.context.active_object
    tuft.data.materials.append(mat_mane)

    # ==========================================
    # 4. CINEMATIC 3-POINT DRAMATIC LIGHTING
    # ==========================================
    # Key Sun (Warm 4800K, low angle)
    bpy.ops.object.light_add(type='SUN', location=(12, -14, 16))
    sun = bpy.context.active_object
    sun.data.energy = 6.2
    sun.data.color = (1.0, 0.90, 0.75)
    sun.data.angle = math.radians(1.8) # Soft organic shadows

    # Cool Rim Light (Sharp backlight defining spine & mane fibers)
    bpy.ops.object.light_add(type='POINT', location=(-10, 10, 6))
    rim = bpy.context.active_object
    rim.data.energy = 950.0
    rim.data.color = (0.35, 0.65, 1.0) # High-contrast cool blue rim

    # Warm Ground Bounce Fill
    bpy.ops.object.light_add(type='POINT', location=(4, 4, 1.2))
    bounce = bpy.context.active_object
    bounce.data.energy = 250.0
    bounce.data.color = (0.8, 0.5, 0.25) # Savanna ground reflection

    # ==========================================
    # 5. PROCEDURAL BREATHING & SWEEP CAMERA
    # ==========================================
    bpy.ops.object.camera_add(location=(0, 8.5, 3.3))
    cam = bpy.context.active_object
    scene.camera = cam

    track = cam.constraints.new(type='TRACK_TO')
    track.target = cranium
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        # Subtle respiratory rise/fall on chest
        chest_breath = 1.15 + 0.04 * math.sin(f * 0.25)
        chest.scale.z = chest_breath
        chest.keyframe_insert(data_path="scale", frame=f)

        # Tail subtle swish
        tail.rotation_euler.y = math.radians(8 * math.sin(f * 0.2))
        tail.keyframe_insert(data_path="rotation_euler", frame=f)

        # Camera orbital pan with elevation descent
        sweep_ang = math.radians(frac * 90.0 - 45.0) # 90 degree focused sweep
        radius = 7.2
        cam.location.x = radius * math.sin(sweep_ang)
        cam.location.y = 2.0 + radius * math.cos(sweep_ang)
        cam.location.z = 3.6 - 0.8 * math.sin(frac * math.pi)
        cam.keyframe_insert(data_path="location", frame=f)

    print("Improved Lion CGI scene setup completed.")

if __name__ == "__main__":
    build_improved_lion_scene()
