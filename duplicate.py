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
from enum import auto, Enum

from .chain import Copy, CreateEmpty, Mirror, Separate, Symmetrize, Target


def deselect_all_vert():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')


def end_process(self, src_shapekey_name):
    deselect_all_vert()
    self.report({'INFO'},
                "WM Sub Tools: {} Shape Key '{}'"
                .format(self.process.name.capitalize(), src_shapekey_name))
    print("Operator '{}' is executed".format(self.bl_idname))

    return {'FINISHED'}


class ProcessKind(Enum):
    copy = auto()
    mirror = auto()
    symmetrize = auto()
    separate = auto()
    blend = auto()


class SAMKSUB_OT_ShapeKeySuperClass(bpy.types.Operator):

    bl_idname = "object.samksub_duplicate_shape_key"
    bl_label = "Duplicate Shape Key"
    bl_description = "Duplicate active shape key"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.copy
    blend_value: bpy.props.FloatProperty(name="Blend Value", default=1.0, min=-2.0, max=2.0)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj.type == 'MESH' and obj.data.shape_keys is not None and context.mode == 'OBJECT'

    def execute(self, context):
        pass


class SAMKSUB_OT_CopyShapeKey(SAMKSUB_OT_ShapeKeySuperClass):

    bl_idname = "object.samksub_copy_shape_key"
    bl_label = "Copy Shape Key"
    bl_description = "Copy active shape key"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.copy

    def execute(self, context):
        active_object = context.active_object
        target = Target(active_object, active_object.active_shape_key.name, 1.0, 0)

        create_empty_handler = CreateEmpty()
        copy_handler = Copy()

        create_empty_handler.set_next(copy_handler)

        create_empty_handler.handle(target)

        return end_process(self, target.src_shapekey_name)


class SAMKSUB_OT_MirrorShapeKey(SAMKSUB_OT_ShapeKeySuperClass):

    bl_idname = "object.samksub_mirror_shape_key"
    bl_label = "Copy & Mirror Shape Key"
    bl_description = "Mirror active shape key"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.mirror

    def execute(self, context):
        active_object = context.active_object
        target = Target(active_object, active_object.active_shape_key.name, 1.0, 0)

        create_empty_handler = CreateEmpty()
        copy_handler = Copy()
        mirror_handler = Mirror()

        create_empty_handler.set_next(copy_handler).set_next(mirror_handler)

        create_empty_handler.handle(target)

        return end_process(self, target.src_shapekey_name)


class SAMKSUB_OT_SymmetrizeShapeKey(SAMKSUB_OT_ShapeKeySuperClass):

    bl_idname = "object.samksub_symmetrize_shape_key"
    bl_label = "Copy & Symmetrize Shape Key"
    bl_description = "Symmetrize active shape key"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.symmetrize

    def execute(self, context):
        active_object = context.active_object
        target = Target(active_object, active_object.active_shape_key.name, 1.0, 0)

        create_empty_handler = CreateEmpty()
        copy_handler = Copy()
        mirror_handler = Mirror()
        symmetrize_handler = Symmetrize()

        create_empty_handler.set_next(copy_handler).set_next(mirror_handler).set_next(symmetrize_handler)

        create_empty_handler.handle(target)

        return end_process(self, target.src_shapekey_name)


class SAMKSUB_OT_SeparateShapeKey(SAMKSUB_OT_ShapeKeySuperClass):

    bl_idname = "object.samksub_separate_shape_key"
    bl_label = "Separate Shape Key"
    bl_description = "Separate active shape key"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.separate

    def execute(self, context):
        active_object = context.active_object
        target = Target(active_object, active_object.active_shape_key.name, 1.0, 0)

        create_empty_handler = CreateEmpty()
        separate_handler = Separate()

        create_empty_handler.set_next(separate_handler)

        create_empty_handler.handle(target)

        return end_process(self, target.src_shapekey_name)


class SAMKSUB_OT_BlendShapeKey(SAMKSUB_OT_ShapeKeySuperClass):

    bl_idname = "object.samksub_blend_shape_key"
    bl_label = "Blend Shape Key by Value"
    bl_description = "Blend active shape key by value"
    bl_options = {'REGISTER', 'UNDO'}

    process = ProcessKind.blend
    blend_value: bpy.props.FloatProperty(name="Blend Value", default=1.0, min=-2.0, max=2.0)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "blend_value")
        layout.separator()

    def execute(self, context):
        active_object = context.active_object
        target = Target(active_object, active_object.active_shape_key.name, self.blend_value, 0)

        create_empty_handler = CreateEmpty()
        copy_handler = Copy()

        create_empty_handler.set_next(copy_handler)

        create_empty_handler.handle(target)

        return end_process(self, target.src_shapekey_name)
