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
import bmesh
from .duplicate import deselect_all_vert


def group_list_func(delimiter, do_group):
    group_name = list()
    for key in bpy.context.active_object.data.shape_keys.key_blocks:
        if do_group and len(delimiter) > 0:
            name_split = key.name.split(delimiter)
            if name_split[0] not in group_name:
                group_name.append(name_split[0])
        else:
            group_name.append(key.name)

    return group_name


def name_in(vgs, *args):
    for i, vg in enumerate(vgs):
        for arg in args:
            if vg.name.startswith(arg) or (vg.name == arg):
                return i
    return None


class SAMKSUB_OT_ApplyToGroup(bpy.types.Operator):

    bl_idname = "object.samksub_apply_to_group"
    bl_label = "Apply To Group"
    bl_description = "Apply to group"
    bl_options = {'REGISTER', 'UNDO'}

    group_list = tuple()
    gl_count = 0

    bv_0: bpy.props.BoolVectorProperty(name="Group 1", description="Group 1", size=32)
    bv_1: bpy.props.BoolVectorProperty(name="Group 2", description="Group 2", size=32)
    bv_2: bpy.props.BoolVectorProperty(name="Group 3", description="Group 3", size=32)
    bv_3: bpy.props.BoolVectorProperty(name="Group 4", description="Group 4", size=32)

    do_group: bpy.props.BoolProperty(name="Group by shape key name", default=True)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj.type == 'MESH' and obj.data.shape_keys is not None and context.mode == 'OBJECT'

    def execute(self, context):
        gl_checked = list()
        bv = [self.bv_0, self.bv_1, self.bv_2, self.bv_3]
        for idx, gl in enumerate(self.group_list):
            j, k = divmod(idx, 32)
            if bv[j][k]:
                gl_checked.append(gl)
        if len(gl_checked) == 0:
            self.report({'INFO'},
                        "WM Sub Tools: Nothing is checkmarked.")
            print("Operator '{}' is executed".format(self.bl_idname))

            return {'FINISHED'}
        gl_checked = tuple(gl_checked)

        obj = bpy.context.active_object
        mesh = obj.data

        data_mesh = bpy.data.meshes[mesh.name]
        data_mesh.use_mirror_x = False
        data_mesh.use_mirror_y = False
        data_mesh.use_mirror_z = False
        data_mesh.use_mirror_topology = False

        mesh.update()
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm_copy = bm.copy()
        bm.faces.ensure_lookup_table()
        bm_copy.faces.ensure_lookup_table()

        keys = mesh.shape_keys.key_blocks
        dst_keys_name = list()
        dst_keys_name = [key.name for key in keys if name_in([key], gl_checked) is not None]

        src_key_ly = bm_copy.verts.layers.shape[obj.active_shape_key.name]
        basis_key_ly = bm_copy.verts.layers.shape['Basis']

        dst_key_lys = list()
        for dst_key_name in dst_keys_name:
            dst_key_lys.append(bm.verts.layers.shape[dst_key_name])

        if 'Basis' in dst_keys_name:
            for key in keys[1:]:
                not_basis_key_ly = bm.verts.layers.shape[key.name]
                for vert, vert_copy in zip(bm.verts, bm_copy.verts):
                    vert[not_basis_key_ly] -= (vert_copy[src_key_ly] - vert_copy[basis_key_ly])

        for idx, dst_key_ly in enumerate(dst_key_lys):
            if 'Basis' in dst_keys_name and idx == 0:
                for vert, vert_copy in zip(bm.verts, bm_copy.verts):
                    vert.co = vert_copy[src_key_ly]
            else:
                for vert, vert_copy in zip(bm.verts, bm_copy.verts):
                    vert[dst_key_ly] += (vert_copy[src_key_ly] - vert_copy[basis_key_ly])

        bm.to_mesh(mesh)
        bm.free()
        bm_copy.free()

        deselect_all_vert()

        self.report({'INFO'},
                    "WM Sub Tools: Apply to group '{}'"
                    .format(bpy.context.active_object.name))
        print("Operator '{}' is executed".format(self.bl_idname))

        return {'FINISHED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        collumn = layout.column(align=True)

        self.group_list = tuple(group_list_func(scene.samksub_delimiter, self.do_group))
        self.gl_count = len(self.group_list)

        if self.gl_count > 128:
            collumn.label(text='WARNING : Number of items is over 128! Could not list all!')
            self.gl_count = 128
        collumn.prop(self, "do_group")

        layout.separator()

        row = layout.row(align=True)

        for i in range(self.gl_count):
            j, k = divmod(i, 32)
            if k == 0:
                collumn = row.column(align=True)
            collumn.prop(self, "bv_" + str(j), text=self.group_list[i], index=k)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=600)
