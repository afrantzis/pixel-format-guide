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

cairo_re = re.compile("CAIRO_FORMAT_(?P<components>[ARGB]+)(?P<total_size>\d+)(?:_(?P<sizes>\d+))?")

cairo_formats = [
    "CAIRO_FORMAT_ARGB32",
    "CAIRO_FORMAT_RGB24",
    "CAIRO_FORMAT_A8",
    "CAIRO_FORMAT_A1",
    "CAIRO_FORMAT_RGB16_565",
    "CAIRO_FORMAT_RGB30",
    ]

def describe(format_str):
    match = cairo_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    total_size_str = match.group("total_size")
    sizes_str = match.group("sizes")

    total_size = int(total_size_str)

    if sizes_str is None:
        component_size = total_size // len(components_str)
        sizes_str = str(component_size) * len(components_str)

    if total_size > 16 and total_size < 32:
        components_str = "X" + components_str
        sizes_str = str(32 - total_size) + sizes_str

    components, sizes = util.parse_components_with_separate_sizes(components_str + sizes_str)
    bits = util.expand_components(components, sizes)

    if len(bits) >= 8:
        memory_le = util.native_to_memory_le(bits)
        memory_be = util.native_to_memory_be(bits)
    else:
        memory_le = util.native_to_memory_byte_le(bits)
        memory_be = util.native_to_memory_byte_be(bits)

    return FormatDescription(
        data_type = "UNORM",
        native = bits,
        memory_le = memory_le,
        memory_be = memory_be)

def formats():
    return cairo_formats

def document():
    return util.read_documentation("cairo.md")
