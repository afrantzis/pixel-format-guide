# Copyright © 2017 Collabora Ltd.
#
# This file is part of pfg.
#
# pfg is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# pfg is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
# more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pfg. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Alexandros Frantzis <alexandros.frantzis@collabora.com>

from . import bgrabitmap
from . import cairo
from . import directfb
from . import drm
from . import opengl
from . import pixman
from . import qt
from . import sdl2
from . import skia
from . import v4l2
from . import vulkan
from . import wayland_drm
from .format_compatibility import FormatCompatibility
from .format_description import FormatDescription

families = [
    bgrabitmap,
    cairo,
    directfb,
    drm,
    opengl,
    pixman,
    qt,
    sdl2,
    skia,
    v4l2,
    vulkan,
    wayland_drm
    ]

def _family_name_from_module(family_module):
    return family_module.__name__.split(".")[-1]

def _family_module_from_name(family_str):
    for f in families:
        modname = _family_name_from_module(f)
        if modname == family_str:
            return f

    return None

def _convert_x_to_a(desc):
    if not desc: return None

    return FormatDescription(
        data_type = desc.data_type,
        native = [bit.replace('X', 'A') for bit in desc.native] if desc.native else None,
        memory_le = [[bit.replace('X', 'A') for bit in byte] for byte in desc.memory_le]
                    if desc.memory_le else None,
        memory_be = [[bit.replace('X', 'A') for bit in byte] for byte in desc.memory_be]
                    if desc.memory_be else None)

def _convert_srgb_to_unorm_in_place(desc):
    if not desc: return

    if desc.data_type == "SRGB":
        desc.data_type = "UNORM"

def describe(format_str):
    for family in families:
        description = family.describe(format_str)
        if description is not None:
            return description

    return None

def document(family_str):
    family = _family_module_from_name(family_str)
    return family.document() if family is not None else None

def find_compatible(format_str, family_str, treat_x_as_a=False,
                    treat_srgb_as_unorm=False, ignore_data_types=False):
    description = describe(format_str)
    if description is None:
        return None

    family = _family_module_from_name(family_str)
    if family is None:
        return None

    family_descriptions = {f:family.describe(f) for f in family.formats()}

    if treat_x_as_a:
        description = _convert_x_to_a(description)
        family_descriptions = {f:_convert_x_to_a(d) for f,d in family_descriptions.items()}

    if treat_srgb_as_unorm:
        _convert_srgb_to_unorm_in_place(description)
        for d in family_descriptions.values():
            _convert_srgb_to_unorm_in_place(d)

    compatibility = FormatCompatibility()

    for name, fd in family_descriptions.items():
        if not ignore_data_types and description.data_type != fd.data_type:
            continue

        if description.native == fd.native and \
           description.memory_le == fd.memory_le and \
           description.memory_be == fd.memory_be:
            compatibility.everywhere.append(name)
        elif description.memory_le == fd.memory_le:
            compatibility.little_endian.append(name)
        elif description.memory_be == fd.memory_be:
            compatibility.big_endian.append(name)

    return compatibility

def list_families():
    return [_family_name_from_module(f) for f in families]

def list_formats(family_str):
    family = _family_module_from_name(family_str)
    if family is None:
        return []

    return family.formats()
