---
name: blender-3d
description: "Blender 3D modeling, animation, scripting, and game asset creation. Use when the user asks about Blender workflows, 3D modeling, UV unwrapping, texturing, materials, shaders, rigging, animation, rendering, Python scripting for Blender, game asset pipelines (Blender to Unity/Unreal/Godot), add-on development, or any 3D art/design task involving Blender."
metadata:
  version: "1.0.0"
  author: "custom"
---

# Blender 3D Workflows

Practical guidance for Blender modeling, animation, scripting, and game asset creation.

## Blender Python Scripting

All Blender operations can be scripted via `bpy`. When writing scripts:

```python
import bpy
import bmesh
from mathutils import Vector, Matrix, Euler
```

### Common Operations

```python
# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create mesh
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
obj = bpy.context.active_object

# Modify mesh with bmesh
bm = bmesh.new()
bm.from_mesh(obj.data)
# ... operations ...
bm.to_mesh(obj.data)
bm.free()

# Materials
mat = bpy.data.materials.new(name="MyMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
obj.data.materials.append(mat)

# Render
bpy.context.scene.render.engine = 'CYCLES'  # or 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.filepath = '/tmp/render.png'
bpy.ops.render.render(write_still=True)
```

### Automation Script Template

When the user wants a Blender script, structure it as:

```python
import bpy
import sys

def main():
    # 1. Setup scene
    # 2. Create/modify objects
    # 3. Apply materials
    # 4. Set up lighting and camera
    # 5. Render or export

if __name__ == "__main__":
    main()
```

Run via: `blender --background --python script.py`

## Modeling Workflow

1. **Block out**: Start with primitives. Get proportions right first.
2. **Topology**: Quads only for deformable meshes. Tris OK for static/game assets.
3. **Edge flow**: Follow muscle/form lines for characters. Clean loops for animation.
4. **Detail**: Subdivision surface modifier → add detail progressively.
5. **Optimize**: Remove unnecessary geometry. Target poly count for use case.

### Poly Count Targets

| Asset type | Target |
|---|---|
| Mobile game prop | 100-1K tris |
| PC game prop | 1K-10K tris |
| Game character (mobile) | 2K-10K tris |
| Game character (PC/console) | 10K-100K tris |
| Film/cinematic | Unlimited (use SubD) |
| Background/LOD | 50-500 tris |

## UV Unwrapping

1. Mark seams in hidden areas (under arms, behind ears, bottom of objects)
2. Unwrap: Smart UV Project for quick results, manual seams for quality
3. Pack islands efficiently (maximize texture space)
4. Straighten UVs for architectural/hard-surface (Follow Active Quads)
5. Check for stretching with UV stretch overlay

## Materials & Shaders (Shader Editor)

PBR workflow:
- **Base Color**: Albedo texture or color
- **Metallic**: 0 for dielectric, 1 for metal (rarely in-between)
- **Roughness**: 0 = mirror, 1 = matte
- **Normal**: Tangent space normal map for surface detail
- **Emission**: For glowing elements

For game export: Principled BSDF maps directly to PBR pipelines.

## Game Asset Pipeline

### Blender → Unity
1. Model in Blender at correct scale (1 Blender unit = 1 meter)
2. Apply all transforms (Ctrl+A → All Transforms)
3. Export as FBX: Forward -Z, Up Y
4. Materials: Bake to textures if using complex node setups
5. Animation: Export with armature, NLA strips for separate anims

### Blender → Unreal Engine
1. Same scale convention (1 unit = 1 cm in UE, set Blender to cm or export with scale)
2. FBX export: Smoothing Face, Apply Modifiers
3. Collisions: Name convention `UCX_MeshName` for custom collision

### Blender → Godot
1. Use glTF 2.0 export (native Godot support)
2. Or save as .blend directly (Godot imports it)
3. Materials map to StandardMaterial3D

## Animation

- **Keyframe basics**: I for insert, auto-key for real-time recording
- **Graph Editor**: F-curves for fine control, handles for easing
- **NLA Editor**: Layer and blend animations, create reusable strips
- **Rigging**: Armature → bone hierarchy → weight paint → constraints
- **Shape Keys**: For facial animation and morph targets

## Rendering

| Engine | Best for | Speed |
|---|---|---|
| Cycles | Photorealism, final renders | Slow (GPU accelerated) |
| EEVEE Next | Real-time preview, stylized | Fast |
| Workbench | Viewport captures, clay renders | Instant |

Optimization: Use denoiser, adaptive sampling, light paths limits, BVH acceleration.

## Add-on Development

```python
bl_info = {
    "name": "My Add-on",
    "blender": (4, 0, 0),
    "category": "Object",
}

class MyOperator(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "My Operator"
    
    def execute(self, context):
        # Your code here
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MyOperator)

def unregister():
    bpy.utils.unregister_class(MyOperator)
```
