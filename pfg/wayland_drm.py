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

from .format_description import FormatDescription
from . import util
import re

wl_drm_re = re.compile("WL_DRM_FORMAT_(?P<components>.*)")

def rgba_bits_to_memory(components):
    return util.native_to_memory_le(components)

def yuv_bits_to_memory(components):
    return util.split_bytes(components)

def describe(format_str):
    match = wl_drm_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)

    if "Y" in components_str:
        memory = yuv_bits_to_memory(bits)
    else:
        memory = rgba_bits_to_memory(bits)

    return FormatDescription(
            native = None,
            memory_le = memory,
            memory_be = memory)

def document():
    return util.read_documentation("wayland_drm.md")
