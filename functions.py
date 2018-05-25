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
        input1 = target_node.inputs.get("Reflection")
        if input1 is None:
            continue
        input1.default_value = scn.abs_reflect * (0.4 if mat.name in ["ABS Plastic Silver", "ABS Plastic Gold"] else 0.01)


def update_abs_fingerprints(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        target_node1 = nodes.get("ABS Dialectric") or nodes.get("ABS Transparent")
        target_node2 = nodes.get("ABS Bump")
        if target_node1 is None or target_node2 is None:
            continue
        input1 = target_node1.inputs.get("Fingerprints")
        input2 = target_node2.inputs.get("Fingerprints")
        if input1 is None or input2 is None:
            continue
        input1.default_value = scn.abs_fingerprints if mat.name not in ["ABS Plastic Silver", "ABS Plastic Gold"] else scn.abs_fingerprints / 8
        input2.default_value = scn.abs_fingerprints * scn.displace



def update_abs_displace(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        target_node = nodes.get("ABS Bump")
        if target_node is None:
            continue
        input1 = target_node.inputs.get("Noise")
        input2 = target_node.inputs.get("Waves")
        if input1 is None or input2 is None:
            continue
        input1.default_value = scn.abs_displace if mat.name not in ["ABS Plastic Silver", "ABS Plastic Gold"] else scn.abs_displace + 0.2
        input2.default_value = scn.abs_displace
        # disconnect displacement node if not used
        color_out = target_node.outputs[0]
        mo_node = nodes.get("Material Output")
        if mo_node is None:
            continue
        displace = mo_node.inputs.get("Displacement")
        if displace is None:
            continue
        if scn.abs_displace == 0:
            for l in displace.links:
                links.remove(l)
        else:
            links.new(target_node.outputs["Color"], displace)


def toggle_save_datablocks(self, context):
    scn = context.scene
    for mat_name in bpy.props.abs_plastic_materials:
        mat = bpy.data.materials.get(mat_name)
        if mat is not None:
            mat.use_fake_user = scn.save_datablocks
