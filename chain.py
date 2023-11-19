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

from dataclasses import dataclass
import bpy
from abc import ABCMeta, abstractmethod


def deselect_all_vert():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

# Chain of Responsibility Pattern


@dataclass
class Target:
    active_object: None
    src_shapekey_name: str
    blend_value: float
    new_shapekey_index: int


class Handler(metaclass=ABCMeta):
    _next = None

    def handle(self, target: Target):
        self.do_process(target)
        if self._next:
            return self._next.handle(target)

    def set_next(self, handler):
        self._next = handler
        return handler

    @abstractmethod
    def do_process(self, target: Target) -> None:
        pass


class CreateEmpty(Handler):
    def do_process(self, target: Target) -> None:
        deselect_all_vert()
        # create empty shapekey
        bpy.ops.object.shape_key_add(from_mix=False)
        target.active_object.active_shape_key.name = target.src_shapekey_name
        target.new_shapekey_index = target.active_object.active_shape_key_index


class Separate(Handler):
    def do_process(self, target: Target) -> None:
        for idx, vert in enumerate(target.active_object.active_shape_key.data):
            if vert.co[0] >= 0.0:
                target.active_object.data.vertices[idx].select = True
            else:
                target.active_object.data.vertices[idx].select = False
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.blend_from_shape(shape=target.src_shapekey_name, blend=1.0, add=False)

        deselect_all_vert()
        target.active_object.active_shape_key.name = target.src_shapekey_name + '.L'
        bpy.ops.object.samksub_mirror_shape_key()
        target.active_object.active_shape_key.name = target.src_shapekey_name + '.R'


class Copy(Handler):
    def do_process(self, target: Target) -> None:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.blend_from_shape(shape=target.src_shapekey_name, blend=target.blend_value, add=False)


class Mirror(Handler):
    def do_process(self, target: Target) -> None:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.shape_key_mirror(use_topology=False)


class Symmetrize(Handler):
    def do_process(self, target: Target) -> None:
        target.active_object.active_shape_key_index = target.new_shapekey_index
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.blend_from_shape(shape=target.src_shapekey_name, blend=1.0, add=True)
