"""
Inspect Blender 3D Lion and Environment scene structure
"""
import os

with open(r"F:\Master AI\07_3D_CGI\scenes\scene_pilot_lion_hero.py", "r") as f:
    code_lion = f.read()

print("=== Lion Hero Script Analysis ===")
print("Armature present:", "armature" in code_lion.lower())
print("Bones present:", "bone" in code_lion.lower())
print("IK constraint present:", "ik" in code_lion.lower())
print("Skinning / Vertex Groups present:", "vertex_groups" in code_lion.lower())
print("Breathing keyframing present:", "chest.keyframe_insert" in code_lion)
print("Head turn keyframing present:", "cranium.keyframe_insert" in code_lion)
print("Tail swish keyframing present:", "tail.keyframe_insert" in code_lion)
print("Hair particle system present:", "particle" in code_lion.lower())
print("Fur Bump normal present:", "bump" in code_lion.lower())
print("Subsurface Scattering present:", "subsurface" in code_lion.lower())

with open(r"F:\Master AI\07_3D_CGI\scenes\scene_pilot_savanna_environment.py", "r") as f:
    code_env = f.read()

print("\n=== Savanna Environment Script Analysis ===")
print("HDRI loading present:", "ShaderNodeTexEnvironment" in code_env)
print("HDRI path referenced:", "aarfontein_sunrise_1k.hdr" in code_env)
print("PBR diffuse texture referenced:", "aerial_ground_rock_diff_1k.jpg" in code_env)
print("PBR texture mapping present:", "ShaderNodeMapping" in code_env)
print("Acacia procedural trees present:", "AcaciaBark" in code_env)
