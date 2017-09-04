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
class LEGOMaterialsPanel(bpy.types.Panel):
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "material"
    bl_label       = "LEGO Materials"
    bl_idname      = "PROPERTIES_LEGO_Materials_append_materials"
    # bl_category    = "LEGO Materials"
    COMPAT_ENGINES = {"CYCLES"}

    @classmethod
    def poll(cls, context):
        """ Only renders UI if cycles render engine is used """
        return bpy.context.scene.render.engine == 'CYCLES'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("scene.append_lego_materials", text="Import LEGO Materials", icon="IMPORT")
        row = col.row(align=True)
        # row.prop(scn, "replaceExisting")