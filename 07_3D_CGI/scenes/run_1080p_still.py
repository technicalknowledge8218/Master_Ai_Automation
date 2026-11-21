
import bpy
import sys
sys.path.append(r'F:\Master AI\07_3D_CGI\scenes')
from scene_benchmark import setup_benchmark_scene
setup_benchmark_scene(res_x=1920, res_y=1080, total_frames=120, samples=16, output_path=r'F:\Master AI\07_3D_CGI\renders\bench_1080p_frame60.png')
bpy.context.scene.frame_current = 60
bpy.context.scene.render.filepath = r'F:\Master AI\07_3D_CGI\renders\bench_1080p_frame60.png'
bpy.ops.render.render(write_still=True)
