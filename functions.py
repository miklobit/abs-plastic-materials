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

def update_abs_subsurf(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        target_node = nodes.get("ABS Dialectric")
        if target_node is None:
            continue
        input1 = target_node.inputs.get("SSS Default")
        input2 = target_node.inputs.get("SSS Amount")
        if input1 is None or input2 is None:
            continue
        default_amount = input1.default_value
        input2.default_value = default_amount * scn.abs_subsurf


def update_abs_reflect(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        target_node = nodes.get("ABS Dialectric") or nodes.get("ABS Transparent")
        if target_node is None:
            continue
        input1 = target_node.inputs.get("Ref Default")
        input2 = target_node.inputs.get("Reflection")
        if input1 is None or input2 is None:
            continue
        default_amount = input1.default_value
        input2.default_value = default_amount * scn.abs_reflect


def update_abs_displace(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        target_node = nodes.get("ABS Bump")
        if target_node is None:
            continue
        input1 = target_node.inputs.get("Default")
        input2 = target_node.inputs.get("Amount")
        if input1 is None or input2 is None:
            continue
        default_amount = input1.default_value
        input2.default_value = default_amount + ((scn.abs_displace - 0.01) / 10)


def toggle_save_datablocks(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is not None:
            mat.use_fake_user = scn.save_datablocks
