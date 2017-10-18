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

class appendABSPlasticMaterials(bpy.types.Operator):
    """Append ABS Plastic Materials from external blender file"""                      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "scene.append_abs_plastic_materials"                                   # unique identifier for buttons and menu items to reference.
    bl_label = "Append ABS Plastic Materials"                                          # display name in the interface.
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scn = context.scene

        # define file paths
        # addonsPath = bpy.utils.user_resource('SCRIPTS', "addons")
        addonPath = os.path.dirname(os.path.abspath(__file__))[:-8]
        blendfile = "%(addonPath)s/abs_plastic_materials.blend" % locals()
        section   = "/Material/"
        directory  = blendfile + section

        # list of materials to append from 'abs_plastic_materials.blend'
        materials = bpy.props.abs_plastic_materials
        alreadyImported = []

        try:
            # set cm.brickMaterialsAreDirty for all models in Rebrickr, if it's installed
            for cm in scn.cmlist:
                if cm.materialType == "Random":
                    cm.brickMaterialsAreDirty = True
        except AttributeError:
            pass

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

            # get the current mode
            current_mode = str(bpy.context.mode)
            # Rename current mode if one of these (for some reason Blender calls them two different things in object.mode_set and context.mode!)
            if current_mode == 'EDIT_MESH': current_mode = 'EDIT'
            if current_mode == 'PAINT_VERTEX': current_mode = 'VERTEX_PAINT'
            if current_mode == 'PAINT_TEXTURE': current_mode = 'TEXTURE_PAINT'
            if current_mode == 'PAINT_WEIGHT': current_mode = 'WEIGHT_PAINT'

            # get the current length of bpy.data.materials
            last_len_mats = len(bpy.data.materials)

            if current_mode != 'OBJECT':
                # switch to object mode
                bpy.ops.object.mode_set(mode='OBJECT')

            # append material from directory
            appendFrom(directory, filename=m)

            if current_mode != 'OBJECT':
                # switch back to last mode
                bpy.ops.object.mode_set(mode=current_mode)

            # get compare last length of bpy.data.materials to current (if the same, material not imported)
            if len(bpy.data.materials) == last_len_mats:
                self.report({"WARNING"}, "'" + m + "' could not be imported. Try reinstalling the addon.")

        # report status
        if len(alreadyImported) == len(materials):
            self.report({"INFO"}, "Materials already imported")
        elif len(alreadyImported) > 0:
            self.report({"INFO"}, "The following Materials were skipped: " + str(alreadyImported)[1:-1].replace("'", "").replace("ABS Plastic ", ""))
        else:
            self.report({"INFO"}, "Materials imported successfully!")

        return{"FINISHED"}
