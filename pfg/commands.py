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

from . import cairo
from . import opengl
from . import pixman
from . import sdl2
from . import v4l2
from . import vulkan
from . import wayland_drm
from .format_compatibility import FormatCompatibility

families = [
    cairo,
    opengl,
    pixman,
    sdl2,
    v4l2,
    vulkan,
    wayland_drm
    ]

def _family_module_from_name(family_str):
    for f in families:
        modname = f.__name__.split(".")[-1]
        if modname == family_str:
            return f

    return None

def describe(format_str):
    for family in families:
        description = family.describe(format_str)
        if description is not None:
            return description

    return None

def document(family_str):
    family = _family_module_from_name(family_str)
    return family.document() if family is not None else None

def find_compatible(format_str, family_str):
    description = describe(format_str)
    if description is None:
        return None

    family = _family_module_from_name(family_str)
    if family is None:
        return None

    family_descriptions = family.describe_all()

    compatibility = FormatCompatibility()

    for name, fd in family_descriptions.items():
        if description.native == fd.native and \
           description.memory_le == fd.memory_le and \
           description.memory_be == fd.memory_be:
            compatibility.everywhere.append(name)
        elif description.memory_le == fd.memory_le:
            compatibility.little_endian.append(name)
        elif description.memory_be == fd.memory_be:
            compatibility.big_endian.append(name)

    return compatibility
