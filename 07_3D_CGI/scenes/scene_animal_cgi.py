import bpy
import math

def build_animal_cgi(
    output_path=r"F:\Master AI\07_3D_CGI\renders\animal_cgi\frame_",
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
    
    # 1. Ground Pedestal / Savanna Mound
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=6.0, depth=0.8, location=(0, 0, -0.4))
    mound = bpy.context.active_object
    mound.name = "SavannaRockMound"
    
    mat_rock = bpy.data.materials.new(name="RockMoundMat")
    mat_rock.use_nodes = True
    b_rock = mat_rock.node_tree.nodes.get("Principled BSDF")
    b_rock.inputs['Base Color'].default_value = (0.35, 0.30, 0.25, 1.0)
    b_rock.inputs['Roughness'].default_value = 0.9
    mound.data.materials.append(mat_rock)
    
    # Materials for Lion
    mat_coat = bpy.data.materials.new(name="LionCoatMat")
    mat_coat.use_nodes = True
    b_coat = mat_coat.node_tree.nodes.get("Principled BSDF")
    b_coat.inputs['Base Color'].default_value = (0.78, 0.58, 0.32, 1.0) # Tawny golden coat
    b_coat.inputs['Roughness'].default_value = 0.65
    b_coat.inputs['Subsurface Weight'].default_value = 0.15 # Organic skin/fur scattering
    
    mat_mane = bpy.data.materials.new(name="LionManeMat")
    mat_mane.use_nodes = True
    b_mane = mat_mane.node_tree.nodes.get("Principled BSDF")
    b_mane.inputs['Base Color'].default_value = (0.28, 0.18, 0.10, 1.0) # Dark amber/brown mane
    b_mane.inputs['Roughness'].default_value = 0.8
    
    # 2. Lion Anatomical Geometry
    # A. Torso / Barrel Chest
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.9, depth=2.8, location=(0, 0, 2.0))
    torso = bpy.context.active_object
    torso.rotation_euler = (math.radians(90), 0, 0)
    torso.scale = (0.9, 1.1, 1.0)
    torso.data.materials.append(mat_coat)
    
    # B. Forequarters & Chest
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.1, location=(0, 1.1, 2.2))
    chest = bpy.context.active_object
    chest.scale = (0.95, 1.0, 1.1)
    chest.data.materials.append(mat_coat)
    
    # C. Hindquarters
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95, location=(0, -1.2, 1.9))
    haunches = bpy.context.active_object
    haunches.data.materials.append(mat_coat)
    
    # D. Four Muscular Limbs
    limb_coords = [(-0.7, 1.0, 1.0), (0.7, 1.0, 1.0), (-0.7, -1.2, 0.9), (0.7, -1.2, 0.9)]
    for lx, ly, lz in limb_coords:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=2.0, location=(lx, ly, lz))
        leg = bpy.context.active_object
        leg.data.materials.append(mat_coat)
        # Paw
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.32, depth=0.25, location=(lx, ly + 0.1, 0.12))
        paw = bpy.context.active_object
        paw.data.materials.append(mat_coat)
        
    # E. Volumetric Layered Mane
    mane_layers = [(0, 1.4, 2.6, 1.45), (0, 1.2, 2.5, 1.6), (0, 0.9, 2.3, 1.7)]
    for mx, my, mz, mrad in mane_layers:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=mrad, location=(mx, my, mz))
        mane_part = bpy.context.active_object
        mane_part.scale = (0.9, 0.75, 1.1)
        mane_part.data.materials.append(mat_mane)
        
    # F. Head & Snout
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.65, location=(0, 2.2, 2.7))
    head = bpy.context.active_object
    head.name = "LionHead"
    head.data.materials.append(mat_coat)
    
    # Snout / Muzzle
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.35, depth=0.6, location=(0, 2.7, 2.5))
    snout = bpy.context.active_object
    snout.rotation_euler = (math.radians(90), 0, 0)
    snout.data.materials.append(mat_coat)
    
    # Ears
    for ex in [-0.5, 0.5]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.18, depth=0.1, location=(ex, 2.1, 3.2))
        ear = bpy.context.active_object
        ear.rotation_euler = (math.radians(45), math.radians(ex * 30), 0)
        ear.data.materials.append(mat_coat)
        
    # G. Tail
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.08, depth=2.2, location=(0, -2.4, 1.4))
    tail = bpy.context.active_object
    tail.rotation_euler = (math.radians(-30), 0, 0)
    tail.data.materials.append(mat_coat)
    
    # 3. Dynamic Studio & Savanna Lighting
    bpy.ops.object.light_add(type='SUN', location=(10, -12, 14))
    sun = bpy.context.active_object
    sun.data.energy = 6.0
    sun.data.color = (1.0, 0.92, 0.80)
    sun.data.angle = math.radians(1.5)
    
    bpy.ops.object.light_add(type='POINT', location=(-8, 8, 5))
    rim = bpy.context.active_object
    rim.data.energy = 700.0
    rim.data.color = (0.4, 0.7, 1.0) # Cool blue rim highlight
    
    # 4. Cinematic Orbital Camera Tracking Head
    bpy.ops.object.camera_add(location=(0, 8.0, 3.2))
    cam = bpy.context.active_object
    scene.camera = cam
    
    track = cam.constraints.new(type='TRACK_TO')
    track.target = head
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    for f in range(1, total_frames + 1):
        frac = f / float(total_frames)
        angle = math.radians(frac * 120.0 - 60.0) # 120 degree sweep
        radius = 6.8
        cam.location.x = radius * math.sin(angle)
        cam.location.y = 1.0 + radius * math.cos(angle)
        cam.location.z = 2.4 + 1.2 * math.sin(frac * math.pi)
        cam.keyframe_insert(data_path="location", frame=f)

if __name__ == "__main__":
    build_animal_cgi()
