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

from . import opengl
from . import vulkan
from . import wayland_drm

families = [
    opengl,
    vulkan,
    wayland_drm
    ]

def describe(format_str):
    for family in families:
        description = family.describe(format_str)
        if description is not None:
            return description

    return None

def document(family):
    for f in families:
        modname = f.__name__.split(".")[-1]
        if modname == family:
            return f.document()
    return None
