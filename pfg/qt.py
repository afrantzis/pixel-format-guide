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

qt_re = re.compile("QImage::Format_(?P<components>[ARGBX]+)(?P<sizes>\d+)(?:_Premultiplied)?")

def _qt_packed(components_str):
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)

    return FormatDescription(
        data_type = "UNORM",
        native = bits,
        memory_le = util.native_to_memory_le(bits),
        memory_be = util.native_to_memory_be(bits))

def _qt_array(components_str):
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)
    memory = util.split_bytes(bits)

    return FormatDescription(
        data_type = "UNORM",
        native = None,
        memory_le = memory,
        memory_be = memory)

def _qt_bit_lsb(components_str):
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)
    memory = util.native_to_memory_byte_le(bits)

    return FormatDescription(
        data_type = "UNORM",
        native = bits,
        memory_le = memory,
        memory_be = memory)

def _qt_bit_msb(components_str):
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)
    memory = util.native_to_memory_byte_be(bits)

    return FormatDescription(
        data_type = "UNORM",
        native = bits,
        memory_le = memory,
        memory_be = memory)

def _normalize_format_str(components_str):
    match = qt_re.match(components_str)
    components_str = match.group("components")
    sizes_str = match.group("sizes")

    sizes = {
        "16" : ["5", "6", "5"],
        "30" : ["2", "10", "10", "10"],
        "32" : ["8", "8", "8", "8"],
    }.get(sizes_str, list(sizes_str))

    total_size = sum((int(s) for s in sizes))
    total_size_proper = util.round_up_to_multiple(total_size, 8)

    if total_size_proper > total_size:
        sizes.insert(0, str(total_size_proper - total_size))

    if len(components_str) < len(sizes):
        components_str = "X" + components_str

    return components_str + "".join(sizes)

qt_formats = {
    "QImage::Format_Mono" : (_qt_bit_msb, "C1"),
    "QImage::Format_MonoLSB" : (_qt_bit_lsb, "C1"),
    "QImage::Format_RGB32" : (_qt_packed, None),
    "QImage::Format_ARGB32" : (_qt_packed, None),
    "QImage::Format_ARGB32_Premultiplied" : (_qt_packed, None),
    "QImage::Format_RGB16" : (_qt_packed, None),
    "QImage::Format_ARGB8565_Premultiplied" : (_qt_packed, None),
    "QImage::Format_RGB666" : (_qt_packed, None),
    "QImage::Format_ARGB6666_Premultiplied" : (_qt_packed, None),
    "QImage::Format_RGB555" : (_qt_packed, None),
    "QImage::Format_ARGB8555_Premultiplied" : (_qt_packed, None),
    "QImage::Format_RGB888" : (_qt_packed, None),
    "QImage::Format_RGB444" : (_qt_packed, None),
    "QImage::Format_ARGB4444_Premultiplied" : (_qt_packed, None),
    "QImage::Format_RGBX8888" : (_qt_array, None),
    "QImage::Format_RGBA8888" : (_qt_array, None),
    "QImage::Format_RGBA8888_Premultiplied" : (_qt_array, None),
    "QImage::Format_BGR30" : (_qt_packed, None),
    "QImage::Format_A2BGR30_Premultiplied" : (_qt_packed, "ABGR2101010"),
    "QImage::Format_RGB30" : (_qt_packed, None),
    "QImage::Format_A2RGB30_Premultiplied" : (_qt_packed, "ARGB2101010"),
    "QImage::Format_Alpha8" : (_qt_packed, "A8"),
    "QImage::Format_Grayscale8" : (_qt_packed, "C8"),
    }

def describe(format_str):
    if not format_str.startswith("QImage::Format"):
        return None

    describe_func, normalized = qt_formats.get(format_str, (None, None))

    if not describe_func:
        return None

    normalized = normalized if normalized else _normalize_format_str(format_str)

    return describe_func(normalized)

def formats():
    return list(qt_formats.keys())

def document():
    return util.read_documentation("qt.md")
