bl_info = {
    "name"        : "ABS Plastic Materials",
    "author"      : "Christopher Gearhart <chris@bblanimation.com>",
    "version"     : (1, 1, 2),
    "blender"     : (2, 79, 0),
    "description" : "Append ABS Plastic Materials to current blender file with a simple click",
    "location"    : "PROPERTIES > Materials > ABS Plastic Materials",
    "warning"     : "",  # used for warning icon and text in addons panel
    "wiki_url"    : "https://www.blendermarket.com/products/abs-plastic-materials",
    "tracker_url" : "https://github.com/bblanimation/abs_plastic_materials/issues",
    "category"    : "Materials"}

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
props = bpy.props

# Addon imports
from .ui import *
from .buttons import *
from .lib import *
from .functions import *

# updater import
from . import addon_updater_ops

def register():
    bpy.utils.register_module(__name__)

    bpy.props.abs_plastic_materials_module_name = __name__

    bpy.props.abs_plastic_materials = [
        'ABS Plastic Black',
        'ABS Plastic Blue',
        'ABS Plastic Bright Green',
        'ABS Plastic Bright Light Orange',
        'ABS Plastic Brown',
        'ABS Plastic Dark Azur',
        'ABS Plastic Dark Brown',
        'ABS Plastic Dark Green',
        'ABS Plastic Dark Grey',
        'ABS Plastic Dark Red',
        'ABS Plastic Dark Tan',
        'ABS Plastic Pearl Gold',
        'ABS Plastic Green',
        'ABS Plastic Light Grey',
        'ABS Plastic Lime',
        'ABS Plastic Orange',
        'ABS Plastic Pink',
        'ABS Plastic Purple',
        'ABS Plastic Red',
        'ABS Plastic Sand Blue',
        'ABS Plastic Sand Green',
        'ABS Plastic Silver',
        'ABS Plastic Tan',
        'ABS Plastic Trans-Clear',
        'ABS Plastic Trans-Yellowish Clear',
        'ABS Plastic Trans-Light Blue',
        'ABS Plastic Trans-Blue',
        'ABS Plastic Trans-Green',
        'ABS Plastic Trans-Light Green',
        'ABS Plastic Trans-Orange',
        'ABS Plastic Trans-Reddish Orange',
        'ABS Plastic Trans-Red',
        'ABS Plastic Trans-Yellow',
        'ABS Plastic White',
        'ABS Plastic Yellow']

    bpy.types.Scene.abs_subsurf = FloatProperty(
        name="Subsurface Scattering",
        description="Amount of subsurface scattering for ABS Plastic Materials (higher values up to 1 are more accurate, but increase render times)",
        min=0, max=10,
        update=update_abs_subsurf,
        default=1)
    bpy.types.Scene.abs_solidReflect = FloatProperty(
        name="Reflection (solid)",
        description="Amount of reflection for solid ABS Plastic Materials",
        min=0, max=100,
        update=updateabs_solidReflect,
        default=1)
    bpy.types.Scene.abs_transReflect = FloatProperty(
        name="Reflection (transparent)",
        description="Amount of reflection for transparent ABS Plastic Materials",
        min=0, max=1,
        update=update_abs_transReflect,
        default=1)
    bpy.types.Scene.abs_displace = FloatProperty(
        name="Displacement",
        description="Bumpiness of the ABS Plastic Materials (mesh must be unwrapped)",
        min=0, max=100,
        update=update_abs_displace,
        default=0.01)

    bpy.types.Scene.isBrickMaterialsInstalled = BoolProperty(default=True)

    # addon updater code and configurations
    addon_updater_ops.register(bl_info)


def unregister():
    Scn = bpy.types.Scene

    # addon updater unregister
    addon_updater_ops.unregister()

    del Scn.isBrickMaterialsInstalled
    del Scn.abs_subsurf
    del bpy.props.abs_plastic_materials
    del bpy.props.abs_plastic_materials_module_name

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
