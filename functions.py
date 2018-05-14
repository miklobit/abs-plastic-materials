"""
Copyright (C) 2017 Bricks Brought to Life
http://bblanimation.com/
chris@bblanimation.com

Created by Christopher Gearhart

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Blender imports
import bpy
from bpy.props import *

# Addon imports
# NONE!

def updateSubsurfAmount(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        ds_node = nodes.get("Diffuse_Subsurf")
        if ds_node is None:
            continue
        print(mat_name)
        mix_amount = float(ds_node.label)
        ds_node.inputs[0].default_value = 1 - (1 - mix_amount) * scn.subsurfAmount
