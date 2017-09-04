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
import os

def appendFrom(directory, filename):
    filepath = directory + filename
    bpy.ops.wm.append(
        filepath=filepath,
        filename=filename,
        directory=directory)

class appendLegoMaterials(bpy.types.Operator):
    """Append LEGO Materials from external blender file"""                      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "scene.append_lego_materials"                                   # unique identifier for buttons and menu items to reference.
    bl_label = "Append LEGO Materials"                                          # display name in the interface.
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scn = context.scene

        # define file paths
        # addonsPath = bpy.utils.user_resource('SCRIPTS', "addons")
        addonPath = os.path.dirname(os.path.abspath(__file__))[:-8]
        blendfile = "%(addonPath)s/lego_materials.blend" % locals()
        section   = "/Material/"
        directory  = blendfile + section

        # list of materials to append from 'lego_materials.blend'
        materials = bpy.props.lego_materials
        alreadyImported = []
        toImport = []
        for m in materials:
            # if material exists, remove or skip
            materialIdx = bpy.data.materials.find(m)
            if materialIdx >= 0:
                if scn.replaceExisting:
                    # remove material
                    bpy.data.materials.remove(bpy.data.materials[materialIdx])
                else:
                    # skip material
                    alreadyImported.append(m)
                    continue
            else:
                toImport.append(m)

            # append material from directory
            newObj = None
            if len(scn.objects) == 0:
                m = bpy.data.meshes.new("junk")
                newObj = bpy.data.objects.new("junk", m)
            current_mode = scn.objects[0].mode
            bpy.ops.object.mode_set(mode='OBJECT')
            appendFrom(directory, filename=m)
            bpy.ops.object.mode_set(mode=current_mode)
            if newObj is not None:
                bpy.data.objects.remove(newObj, True)
                bpy.data.meshes.remove(m, True)

        if len(alreadyImported) > 0:
            self.report({"INFO"}, "The following Materials were skipped: " + str(alreadyImported)[1:-1].replace("'", "").replace("LEGO Plastic ", ""))

        return{"FINISHED"}
