# Copyright (C) 2021 SyureOjisan
#
# This file is part of WM Sub Tools.
#
# WM Sub Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WM Sub Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WM Sub Tools.  If not, see <http://www.gnu.org/licenses/>.

import bpy


class SAMKSUB_OT_PasteVGroup(bpy.types.Operator):

    bl_idname = "object.samksub_paste_vgroup"
    bl_label = "Paste Weight"
    bl_description = "Paste Weight Active To Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.vertex_weight_copy()
        self.report({'INFO'},
                    "WM Sub Tools: Paste Weight Active To Selected")
        print("Operator '{}' is executed".format(self.bl_idname))

        return {'FINISHED'}
