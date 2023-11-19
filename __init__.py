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


bl_info = {
    "name": "WM Sub Tools",
    "author": "SyureOjisan",
    "version": (0, 1, 3),  # big modifying, small modifying, bug fix or refactoring
    "blender": (2, 80, 0),
    "location": "Properties > Object Data Properties",
    "description": "WM Sub Tools",
    "warning": "",
    "support": 'COMMUNITY',
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


if "bpy" in locals():
    import imp
    imp.reload(apply)
    imp.reload(chain)
    imp.reload(duplicate)
    imp.reload(paste)
    imp.reload(preferences)
else:
    from . import apply
    from . import chain
    from . import duplicate
    from . import paste
    from . import preferences


import bpy


def menu_fn_shape_key(self, context):
    self.layout.separator()
    self.layout.operator(duplicate.SAMKSUB_OT_CopyShapeKey.bl_idname)
    self.layout.operator(duplicate.SAMKSUB_OT_MirrorShapeKey.bl_idname)
    self.layout.operator(duplicate.SAMKSUB_OT_SymmetrizeShapeKey.bl_idname)
    self.layout.operator(duplicate.SAMKSUB_OT_SeparateShapeKey.bl_idname)
    self.layout.operator(duplicate.SAMKSUB_OT_BlendShapeKey.bl_idname)
    self.layout.operator(apply.SAMKSUB_OT_ApplyToGroup.bl_idname)


def menu_fn_mesh_mode(self, context):
    self.layout.separator()
    self.layout.operator(paste.SAMKSUB_OT_PasteVGroup.bl_idname)


classes_shape_key = [
    duplicate.SAMKSUB_OT_CopyShapeKey,
    duplicate.SAMKSUB_OT_MirrorShapeKey,
    duplicate.SAMKSUB_OT_SymmetrizeShapeKey,
    duplicate.SAMKSUB_OT_SeparateShapeKey,
    duplicate.SAMKSUB_OT_BlendShapeKey,
    apply.SAMKSUB_OT_ApplyToGroup,
]

classes_mesh_mode = [
    paste.SAMKSUB_OT_PasteVGroup,
]

classes = [
    preferences.SAMKSUB_Preferences,
]


# プロパティの初期化
def init_props():
    scene = bpy.types.Scene
    scene.samksub_delimiter = bpy.props.StringProperty(
        name="Delimiter",
        description="Delimiter",
        default='.',
    )


# プロパティを削除
def clear_props():
    scene = bpy.types.Scene
    del scene.samksub_delimiter


def register():
    for c in classes_shape_key:
        bpy.utils.register_class(c)
    bpy.types.MESH_MT_shape_key_context_menu.append(menu_fn_shape_key)

    for c in classes_mesh_mode:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_fn_mesh_mode)

    for c in classes:
        bpy.utils.register_class(c)

    init_props()

    print("Add-on '{}' is enabled".format(bl_info["name"]))


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(menu_fn_shape_key)
    for c in classes_shape_key:
        bpy.utils.unregister_class(c)

    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_fn_mesh_mode)
    for c in classes_mesh_mode:
        bpy.utils.unregister_class(c)

    for c in classes:
        bpy.utils.unregister_class(c)

    clear_props()

    print("Add-on '{}' is disabled".format(bl_info["name"]))


if __name__ == "__main__":
    register()
