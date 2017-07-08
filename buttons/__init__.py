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
        materials = [
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
            'LEGO Plastic Light Bluish Green',
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
            appendFrom(directory, filename=m)

        if len(alreadyImported) > 0:
            self.report({"WARNING"}, "The following Materials were skipped: " + str(alreadyImported)[1:-1].replace("'", "").replace("LEGO Plastic ", ""))

        return{"FINISHED"}
