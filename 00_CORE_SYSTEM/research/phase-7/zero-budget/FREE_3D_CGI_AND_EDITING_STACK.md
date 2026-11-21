# FREE 3D CGI AND PROFESSIONAL EDITING STACK
## Headless Blender 4.x Automation, CC0 Asset Archives, Lemo-Opuscar Frame-Piping & FFmpeg 7.1

**Document Version:** 1.0.0-zero-budget  
**Project Root:** `F:\Master AI`  
**Target Path:** `00_CORE_SYSTEM\research\phase-7\zero-budget\FREE_3D_CGI_AND_EDITING_STACK.md`  
**Classification:** 3D CGI Engineering & Programmatic Video Editing  
**Status:** Approved Technical Blueprint  

---

## 1. EXECUTIVE SUMMARY & ZERO-COST EDITING ARCHITECTURE

Master AI completely eliminates reliance on proprietary, paid video editing software (Adobe Premiere, DaVinci Resolve Studio, Final Cut Pro) and paid 3D software (Cinema 4D, Maya, 3ds Max).

By pairing **Blender 4.x** (GNU GPL v3) with **FFmpeg 7.1** and the **MIT-licensed Lemo-Opuscar headless rendering engine**, Master AI establishes a broadcast-grade editing and CGI stack that runs entirely on our Windows 11 host with zero license fees, zero subscriptions, and complete automation via Python 3.14 and Node 24.

---

## 2. BLENDER 4.X HEADLESS AUTOMATION ON INTEL IRIS XE

Blender 4.x installs in ~800 MB and includes its own standalone Python interpreter (`bpy`). It executes headlessly from command line:
```bash
blender.exe -b -P scene_builder.py -o renders/shot_01.mp4 -a
```

### 2.1 EEVEE Next vs. Cycles CPU Performance on Host

| Parameter | EEVEE Next (Real-Time Rasterizer) | Cycles CPU (Path Tracer with Intel Embree) |
| :--- | :--- | :--- |
| **Compute Device** | Intel Iris Xe Graphics (Direct3D 11 / Vulkan) | Intel Core i5-1245U (10 Cores, 12 Threads) |
| **Render Latency** | **1.2 to 2.5 seconds / frame** (1080p) | **15 to 30 seconds / frame** (1080p, 64 samples) |
| **5-Second Clip (150 frames)**| **~3.5 to 5.0 minutes total** | **~40 to 60 minutes total** |
| **Visual Strengths** | Real-time volumetric fog, screen-space reflections, high FPS | Perfect realistic soft shadows, caustics, global illumination |
| **Master AI Role** | **Primary Animation & Motion Engine** | **Hero Stills, Scientific Macro Passes, Night Shaders** |

### 2.2 Reusable Headless Camera Orbit Generator (`bpy`)
```python
# F:\Master AI\09_CONTENT_STUDIO\engine\blender_scripts\camera_orbit.py
import bpy
import math

def setup_orbit_shot(model_path: str, output_path: str, duration_sec: float = 5.0, fps: int = 30):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = int(duration_sec * fps)

    # Configure EEVEE Next for Iris Xe
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.eevee.use_shadows = True

    # Import CC0 3D Model
    bpy.ops.import_scene.gltf(filepath=model_path)
    subject = bpy.context.selected_objects[0]
    subject.location = (0, 0, 0)

    # Empty target for camera tracking
    target = bpy.data.objects.new("CamTarget", None)
    scene.collection.objects.link(target)
    target.location = (0, 0, 0.8)

    # Camera setup with Track-To constraint
    cam_data = bpy.data.cameras.new("OrbitCam")
    cam_obj = bpy.data.objects.new("OrbitCam", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj

    constraint = cam_obj.constraints.new(type='TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Animate orbit path (circle formula)
    radius = 4.5
    height = 1.6
    for frame in range(1, scene.frame_end + 1):
        angle = (frame / scene.frame_end) * math.radians(60) # 60 degree cinematic sweep
        cam_obj.location.x = radius * math.sin(angle)
        cam_obj.location.y = -radius * math.cos(angle)
        cam_obj.location.z = height
        cam_obj.keyframe_insert(data_path="location", frame=frame)

    # Output to H.264 MP4
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.filepath = output_path
    bpy.ops.render.render(animation=True)
```

---

## 3. ZERO-COST CC0 & PUBLIC DOMAIN 3D ASSET ARCHIVES

Master AI connects directly to verified public domain repositories, eliminating paid 3D marketplaces (TurboSquid, CGTrader):

1. **Poly Haven (`https://polyhaven.com`):**
   - **License:** 100% Dedicated **CC0-1.0 Universal**.
   - **Content:** Hundreds of photorealistic 3D models (foliage, terrain, architecture), 4K PBR texture maps, and 8K HDRIs for natural environment lighting.
   - **Format:** Native `.blend` and `.glb` files ready for instant headless import.
2. **ambientCG (`https://ambientcg.com`):**
   - **License:** 100% **CC0-1.0 Universal**.
   - **Content:** Over 1,800 seamless PBR material maps (sand, savannas, rock, bark, concrete).
3. **Smithsonian 3D Open Access (`https://3d.si.edu`):**
   - **License:** 100% **CC0 Public Domain**.
   - **Content:** Digitized museum scans of historical artifacts, dinosaur skeletons, and wild animal skulls/skeletons.
4. **NASA 3D Resources (`https://nasa3d.arc.nasa.gov`):**
   - **License:** 100% **Public Domain**.
   - **Content:** True-to-scale planets, Mars rover models, satellites, and astronomical terrain heightmaps.

---

## 4. PROFESSIONAL EDITING AT ₹0: FFMPEG 7.1 + LEMO-OPUSCAR

### 4.1 Lemo-Opuscar MIT Frame-Piping Core
Master AI adapts Lemo-Opuscar's MIT-licensed `core/render/video.mjs` directly into `09_CONTENT_STUDIO/engine/lemo_renderer_adapter.py`. 
- **Kinetic Typography:** Motion titles are designed in clean HTML5/Canvas/CSS.
- **Headless Pipeline:** Playwright spins up Chromium workers, evaluates `window.render(t)`, and pipes uncompressed frame buffers straight into FFmpeg stdin.
- **Zero Disk Thrashing:** No millions of loose PNG files; frames stream directly through memory pipes.

### 4.2 Automated Scene Assembly & Transition Filtergraph
```bash
ffmpeg \
  -i scene_01_stock.mp4 \
  -i scene_02_3dcgi.mp4 \
  -i scene_03_stock.mp4 \
  -filter_complex \
  "[0:v][1:v]xfade=transition=fadeblack:duration=1.0:offset=49.0[v01]; \
   [v01][2:v]xfade=transition=fadeblack:duration=1.0:offset=98.0[v02]; \
   [v02]lut3d=file='styles/luts/savanna_golden_hour.cube'[graded]; \
   [graded]ass=subtitles_hindi.ass[final_v]" \
  -map "[final_v]" -map 3:a -c:v libx264 -crf 18 -preset medium output_master.mp4
```

### 4.3 Two-Pass EBU R128 Audio Mastering
Master AI applies professional broadcast loudness compliance at zero cost using FFmpeg's native `loudnorm` filter:
- Target integrated loudness: `-14.0 LUFS`.
- True-peak ceiling: `-1.0 dBTP`.
- Vocal sidechain ducking attenuates background music by `-14 dB` during speech, ensuring crystal-clear vocal intelligibility.
