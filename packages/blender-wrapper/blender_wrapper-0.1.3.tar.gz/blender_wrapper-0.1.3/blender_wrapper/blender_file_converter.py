
import bpy
import sys
from os.path import dirname

# add the utils directory to sys.path
sys.path.append(dirname(__file__))

from blender_utils.blender_context_manager import mesh_edit  # noqa
from blender_utils.blender_file_loader import parse_args  # noqa

param = parse_args()

print(f'Convert format: {param.file_path} to: {param.export_path}')

with mesh_edit(mesh_name=param.mesh_name) as bm:

    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles()

param.export()
