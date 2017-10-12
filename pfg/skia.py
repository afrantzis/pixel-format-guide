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

_array = 0
_packed = 1

skia_formats = {
    "kAlpha_8_SkColorType" : ("A8", _array),
    "kRGB_565_SkColorType" : ("R5G6B5", _packed),
    "kARGB_4444_SkColorType" : ("R4G4B4A4", _packed),
    "kRGBA_8888_SkColorType" : ("R8G8B8A8", _array),
    "kBGRA_8888_SkColorType" : ("B8G8R8A8", _array),
    "kGray_8_SkColorType," : ("C8", _array),
    "kRGBA_F16_SkColorType" : ("R16G16B16A16", _array),
    }

def describe(format_str):
    normalized, normalized_type = skia_formats.get(format_str, (None, None))
    if not normalized:
        return None

    components, sizes = util.parse_components_with_mixed_sizes(normalized)
    bits = util.expand_components(components, sizes)

    if normalized_type == _array:
        memory = util.split_bytes_le(bits, sizes[0] // 8)
    else:
        memory = util.native_to_memory_le(bits)

    return FormatDescription(
        data_type = "SFLOAT" if "F" in format_str else "UNORM",
        native = None,
        memory_le = memory,
        memory_be = None)

def formats():
    return list(skia_formats.keys())

def document():
    return util.read_documentation("skia.md")
