"""
Copyright (C) 2018 Bricks Brought to Life
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

# System imports
# NONE!

# Blender imports
import bpy
from bpy.app.handlers import persistent
from mathutils import Vector, Euler

# Addon imports
# NONE!


@persistent
def handle_upconversion(scene):
    scn = bpy.context.scene
    # rename outdated 'ABS Plastic Pink' to 'ABS Plastic Bright Pink'
    pinkMat = bpy.data.materials.get('ABS Plastic Pink')
    if pinkMat is not None:
        pinkMat.name = 'ABS Plastic Bright Pink'

bpy.app.handlers.load_post.append(handle_upconversion)
