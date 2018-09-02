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

from ..functions import *
from ..colors import *

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

    @classmethod
    def poll(self, context):
        return context.scene.render.engine == 'CYCLES'

    def execute(self, context):
        scn = context.scene

        # define file paths
        # addonsPath = bpy.utils.user_resource('SCRIPTS', "addons")
        addonPath = os.path.dirname(os.path.abspath(__file__))[:-8]
        blendfile = "%(addonPath)s/abs_plastic_materials.blend" % locals()
        section   = "/Material/"
        directory  = blendfile + section

        # list of materials to append from 'abs_plastic_materials.blend'
        mat_names = getMatNames()
        alreadyImported = []
        matsToReplace = []
        failed = []

        imagesToReplace = ["ABS Fingerprints and Dust"]
        nodeGroupsToReplace = ["Dialectric", "Transparent", "Bump", "Uniform Scale"]

        try:
            # set cm.brickMaterialsAreDirty for all models in Rebrickr, if it's installed
            for cm in scn.cmlist:
                if cm.materialType == "Random":
                    cm.brickMaterialsAreDirty = True
        except AttributeError:
            pass

        # remove existing bump/specular maps
        for im in bpy.data.images:
            if im.name in imagesToReplace:
                bpy.data.images.remove(im)
        # remove old existing node groups
        for ng in bpy.data.node_groups:
            if ng.name.startswith("ABS_") and ng.name[4:] in nodeGroupsToReplace:
                bpy.data.node_groups.remove(ng)

        # get the current mode
        current_mode = str(bpy.context.mode)
        # Rename current mode if one of these (for some reason Blender calls them two different things in object.mode_set and context.mode!)
        if current_mode == 'EDIT_MESH': current_mode = 'EDIT'
        if current_mode == 'PAINT_VERTEX': current_mode = 'VERTEX_PAINT'
        if current_mode == 'PAINT_TEXTURE': current_mode = 'TEXTURE_PAINT'
        if current_mode == 'PAINT_WEIGHT': current_mode = 'WEIGHT_PAINT'

        # temporarily switch to object mode
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        for mat_name in mat_names:
            # if material exists, remove or skip
            m = bpy.data.materials.get(mat_name)
            if m is not None:
                # mark material to replace
                m = bpy.data.materials.get(mat_name)
                m.name = m.name + "__replaced"
                matsToReplace.append(m)

            # get the current length of bpy.data.materials
            last_len_mats = len(bpy.data.materials)

            # append material from directory
            appendFrom(directory, filename=mat_name)

            # get compare last length of bpy.data.materials to current (if the same, material not imported)
            if len(bpy.data.materials) == last_len_mats:
                self.report({"WARNING"}, "'%(mat_name)s' could not be imported. Try reinstalling the addon." % locals())
                if m in matsToReplace:
                    matsToReplace.remove(m)
                failed.append(mat_name)
                continue

            # # ensure material saves to blender file
            # new_mat = bpy.data.materials.get(m)
            # new_mat.use_fake_user = True

        # replace old material node trees
        for old_mat in matsToReplace:
            origName = old_mat.name.split("__")[0]
            new_mat = bpy.data.materials.get(origName)
            old_mat.user_remap(new_mat)
            bpy.data.materials.remove(old_mat)

        # switch back to last mode
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=current_mode)

        # update subsurf/reflection amounts
        update_abs_subsurf(self, bpy.context)
        update_abs_reflect(self, bpy.context)
        update_abs_randomize(self, bpy.context)
        update_abs_fingerprints(self, context)
        update_abs_displace(self, bpy.context)
        toggle_save_datablocks(self, bpy.context)

        # remap bump/specular to one im
        for mapName in imagesToReplace:
            firstIm = None
            for im in bpy.data.images:
                if im is None:
                    continue
                if im.name.startswith(mapName):
                    if im.users == 0:
                        bpy.data.images.remove(im)
                    elif firstIm is None:
                        firstIm = im
                    else:
                        im.user_remap(firstIm)
                        bpy.data.images.remove(im)
            if firstIm is not None:
                firstIm.name = mapName

        # remap node groups to one group
        for groupName in nodeGroupsToReplace:
            groupName = "ABS_" + groupName
            firstGroup = None
            for g in bpy.data.node_groups:
                if g is None:
                    continue
                if g.name.startswith(groupName):
                    if g.users == 0:
                        bpy.data.node_groups.remove(g)
                    elif firstGroup is None:
                        firstGroup = g
                    else:
                        g.user_remap(firstGroup)
                        bpy.data.node_groups.remove(g)
            if firstGroup is not None:
                firstGroup.name = groupName

        # report status
        if len(alreadyImported) == len(mat_names):
            self.report({"INFO"}, "Materials already imported")
        elif len(alreadyImported) > 0:
            self.report({"INFO"}, "The following Materials were skipped: " + str(alreadyImported)[1:-1].replace("'", "").replace("ABS Plastic ", ""))
        elif len(failed) > 0:
            self.report({"INFO"}, "The following Materials failed to import (try reinstalling the addon): " + str(failed)[1:-1].replace("'", "").replace("ABS Plastic ", ""))
        else:
            self.report({"INFO"}, "Materials imported successfully!")

        return{"FINISHED"}
