bl_info = {
    "name"        : "LEGO Materials",
    "author"      : "Christopher Gearhart <chris@bblanimation.com>",
    "version"     : (0, 1, 0),
    "blender"     : (2, 78, 0),
    "description" : "Append LEGO Materials to current blender file with a simple click",
    "location"    : "PROPERTIES > Materials > LEGO Materials",
    # "warning"     : "Work in progress",
    "wiki_url"    : "",
    "tracker_url" : "",
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

# system imports
import bpy
from bpy.props import *
from .ui import *
from .buttons import *
props = bpy.props

def register():
    bpy.utils.register_module(__name__)

    bpy.props.lego_materials = [
        'LEGO Plastic Black',
        'LEGO Plastic Blue',
        'LEGO Plastic Bright Green',
        'LEGO Plastic Brown',
        'LEGO Plastic Dark Azur',
        'LEGO Plastic Dark Green',
        'LEGO Plastic Dark Grey',
        'LEGO Plastic Dark Red',
        'LEGO Plastic Gold',
        'LEGO Plastic Green',
        'LEGO Plastic Light Bluish Grey',
        'LEGO Plastic Light Grey',
        'LEGO Plastic Lime',
        'LEGO Plastic Orange',
        'LEGO Plastic Pink',
        'LEGO Plastic Purple',
        'LEGO Plastic Red',
        'LEGO Plastic Tan',
        'LEGO Plastic Trans-Blue',
        'LEGO Plastic Trans-Clear',
        'LEGO Plastic Trans-Light Green',
        'LEGO Plastic Trans-Red',
        'LEGO Plastic Trans-Yellow',
        'LEGO Plastic White',
        'LEGO Plastic Yellow']

    bpy.types.Scene.replaceExisting = BoolProperty(
        name="Replace Existing",
        description="Replace existing 'LEGO Plastic *' materials when importing",
        default=False)

def unregister():
    Scn = bpy.types.Scene

    del Scn.replaceExisting

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
