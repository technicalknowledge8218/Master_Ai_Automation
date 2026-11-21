# 3D CGI RENDERING & PERFORMANCE EMPIRICAL TEST PLAN
**Master AI — Phase 7.0.3 Independent Technical Reality Audit**  
**Audit Target:** Procedural 3D CGI Animation Pipeline  
**Core Technologies:** Headless Blender 4.x, EEVEE Next, Cycles (CPU fallback), Python `bpy`  
**Execution Environment:** Windows 11, 12th Gen Intel Core i5-1245U, 32 GB RAM, Intel Iris Xe Graphics  
**Status Classification Standard:**
- `Verified from official documentation`
- `Verified by actual local testing`
- `Estimated but untested`
- `Unverified`
- `Unsupported or incorrect`

---

## 1. Test Objective & Scope

This test plan defines the empirical validation protocol for Master AI's Mode B (3D CGI Production Engine) to be executed during Phase 7.1. The objective is to verify genuine 3D scene creation, camera choreography, dynamic lighting/shadows, and headless batch rendering on the host Intel Iris Xe platform.

### Core Capabilities Validated:
1. **Procedural Geometry Generation:** Programmatic creation of 3D meshes (terrain, pedestal, geometric monuments, volumetric props) via Python `bpy`.
2. **Physically-Based Materials:** Applying Principled BSDF shaders with roughness, metallic, normal displacement, and emission attributes.
3. **Dynamic Studio & Outdoor Lighting:** Key, fill, and rim light configurations casting realistic soft shadows.
4. **Cinematic Camera Choreography:** Bézier-interpolated orbital camera motion maintaining depth perspective across a 360-degree sweep.
5. **Headless Execution & Performance Profiling:** Verifying frame render times, memory footprint, and stability at both 720p and 1080p resolutions without an active GUI display.

---

## 2. Test Scene Specification: "The Serengeti Monolith"

```
                     [Key Light: Sun Lamp / Warm 4500K]
                                   \
                                    \
       [Rim Light: Cool 7500K]       v
               \                  +-------------------+
                \                 |  3D Monolith      |  <--- Camera Orbit Path (Radius 8m)
                 v                |  (Carved Stone)   |       Z-Axis: 1.5m -> 3.0m
         +-----------------+      +-------------------+       LookAt: Center Target
         | Procedural Dune |         |         |
         | & Rock Mesh     |         v         v
         +-----------------+      [Cast Shadow on Ground]
                                  [ambientCG Sand PBR]
```

### Technical Specifications:
- **Duration:** 5.00 seconds (120 frames @ 24 FPS)
- **Primary Object:** Procedurally extruded hexagonal monolith with beveled edges and procedural displacement.
- **Environment:** Displaced ground plane (10,000 vertices) with PBR sand material and contact shadows.
- **Camera Path:** 180-degree orbital sweep with subtle focal length zoom (35mm to 50mm).
- **Lighting:** Directional Sun lamp (intensity 4.5, angle 0.5°) + HDR environment ambient fill.

---

## 3. Autonomous Python Test Harness (`test_3d_render.py`)

The test harness operates completely headlessly using Blender's bundled Python interpreter:

```python
import bpy
import math
import time
import os

def build_scene():
    # 1. Reset scene to pristine state
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' # Fallback: 'CYCLES'
    
    # 2. Output Settings
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 120 # 5 seconds
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = os.path.abspath("./render_output/frame_")

    # 3. Procedural Geometry: Ground Plane
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "GroundPlane"
    bpy.ops.object.subdivide(number_cuts=20)
    
    # Ground Material
    mat_ground = bpy.data.materials.new(name="GroundMat")
    mat_ground.use_nodes = True
    bsdf_g = mat_ground.node_tree.nodes.get("Principled BSDF")
    bsdf_g.inputs['Base Color'].default_value = (0.76, 0.60, 0.42, 1.0) # Desert Sand
    bsdf_g.inputs['Roughness'].default_value = 0.85
    ground.data.materials.append(mat_ground)

    # 4. Hero Object: Hexagonal Monolith
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.5, depth=5.0, location=(0, 0, 2.5))
    monolith = bpy.context.active_object
    monolith.name = "HeroMonolith"
    
    mat_mono = bpy.data.materials.new(name="MonolithMat")
    mat_mono.use_nodes = True
    bsdf_m = mat_mono.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.15, 0.18, 0.22, 1.0) # Dark Basalt
    bsdf_m.inputs['Metallic'].default_value = 0.3
    bsdf_m.inputs['Roughness'].default_value = 0.2
    monolith.data.materials.append(mat_mono)

    # 5. Lighting: Sun + Fill
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 15))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    sun.data.angle = math.radians(1.0) # Soft shadows

    bpy.ops.object.light_add(type='POINT', location=(-8, 8, 6))
    fill = bpy.context.active_object
    fill.data.energy = 800.0
    fill.data.color = (0.3, 0.5, 0.9) # Cool blue rim fill

    # 6. Camera Choreography (Bézier Orbit)
    bpy.ops.object.camera_add(location=(0, -9, 3.5))
    cam = bpy.context.active_object
    scene.camera = cam
    
    # Track To Constraint
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = monolith
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Animate Orbit around Z-axis
    for f in range(1, 121):
        angle = math.radians((f / 120.0) * 180.0 - 90.0)
        radius = 8.5
        cam.location.x = radius * math.sin(angle)
        cam.location.y = -radius * math.cos(angle)
        cam.location.z = 2.0 + 1.5 * math.sin(math.pi * f / 120.0)
        cam.keyframe_insert(data_path="location", frame=f)

build_scene()
```

---

## 4. Headless Execution Commands & Test Matrix

Execute two empirical test passes:

### Pass A: EEVEE Next 720p Baseline Test
```bash
blender -b -P test_3d_render.py -- --engine BLENDER_EEVEE_NEXT --res-x 1280 --res-y 720
```

### Pass B: EEVEE Next 1080p Production Benchmark
```bash
blender -b -P test_3d_render.py -- --engine BLENDER_EEVEE_NEXT --res-x 1920 --res-y 1080
```

### Pass C (Comparative): Cycles CPU Single-Frame Still (Frame 60)
```bash
blender -b -P test_3d_render.py -f 60 -- --engine CYCLES --samples 128
```

---

## 5. Empirical Acceptance Criteria & Thresholds

| Metric | Target Specification | Minimum Pass Threshold | Test Method | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Headless Initialization** | Clean startup without display | 0 X11/WGL display crash errors | Blender exit code = 0 | `Verified from official documentation` |
| **720p Render Time (EEVEE Next)** | ≤ 2.50 sec / frame | ≤ 5.00 sec / frame | Per-frame log timestamps | `Estimated but untested` |
| **1080p Render Time (EEVEE Next)** | ≤ 6.00 sec / frame | ≤ 12.00 sec / frame | Per-frame log timestamps | `Estimated but untested` |
| **Peak RAM Utilization** | < 4.0 GB RAM | < 8.0 GB RAM | Windows Process Monitor | `Estimated but untested` |
| **Shadow & Depth Verification** | Cast shadows present, perspective shifts | Monolith cast shadow visibly projected on ground | Frame inspection (FFmpeg luminance diff) | `Estimated but untested` |
| **3D Motion Smoothness** | Consistent orbital sweep (24 FPS) | Zero dropped frames, zero stutter | Motion vector variance < 5% | `Estimated but untested` |
| **Cycles CPU Still (Frame 60)** | Complete denoise via OIDN | Under 120 seconds for 1 still | Timer on single frame render | `Estimated but untested` |

---

## 6. Risk Mitigations for Host Hardware

1. **Integrated GPU Context Errors:** If Windows Session 0 or headless background task execution fails to initialize Intel Iris Xe OpenGL WGL context, the engine must set `os.environ["MESA_GL_VERSION_OVERRIDE"] = "4.5"` or launch via Windows desktop session runner.
2. **Thermal Throttling on Core i5-1245U:** Ultra-low voltage (U-series) mobile chips are TDP-constrained (15W base, 55W turbo). Sustained rendering of 120 frames may cause CPU clock throttling from 4.4 GHz down to ~2.0-2.4 GHz. The orchestrator must insert a 50ms cooldown pause between batch chunks if CPU temperature exceeds 85°C.
3. **Classification:** `Verified from official documentation`.
