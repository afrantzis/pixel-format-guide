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
import math

v4l2_re = re.compile("V4L2_PIX_FMT_(?P<components>[RGBAX]+)(?P<sizes>\d+)(?P<x>X)?")

v4l2_formats = [
    "V4L2_PIX_FMT_RGB332",
    "V4L2_PIX_FMT_ARGB444",
    "V4L2_PIX_FMT_XRGB444",
    "V4L2_PIX_FMT_ARGB555",
    "V4L2_PIX_FMT_XRGB555",
    "V4L2_PIX_FMT_RGB565",
    "V4L2_PIX_FMT_ARGB555X",
    "V4L2_PIX_FMT_XRGB555X",
    "V4L2_PIX_FMT_RGB565X",
    "V4L2_PIX_FMT_BGR24",
    "V4L2_PIX_FMT_RGB24",
    "V4L2_PIX_FMT_BGR666",
    "V4L2_PIX_FMT_ABGR32",
    "V4L2_PIX_FMT_XBGR32",
    "V4L2_PIX_FMT_ARGB32",
    "V4L2_PIX_FMT_XRGB32",
    ]

def describe_bgr666():
    memory = [
        util.component_bits("B", 5, 0) + util.component_bits("G", 5, 4),
        util.component_bits("G", 3, 0) + util.component_bits("R", 5, 2),
        util.component_bits("R", 1, 0) + util.component_bits("X", 5, 0)]
    return FormatDescription(
        data_type = "UNORM",
        native = None,
        memory_le = memory,
        memory_be = memory)

# Normalize bits string to contain bit values for all components
def normalize_sizes_str(components_str, sizes_str):
    if sizes_str == "32":
        sizes_str = "8888"
    elif sizes_str == "24":
        sizes_str = "888"

    # The size of the A/X component is not explicitly specified; we need to
    # infer it from the components, the specified bits and the size of the
    # native type (which is always a multiple of 8 bits)
    if "X" in components_str or "A" in components_str:
        specified_bits = sum([int(i) for i in sizes_str])
        format_bits = int(math.ceil(specified_bits / 8) * 8)
        extra_bits = format_bits - specified_bits
        # The A/X component is always at the beginning of the component_str
        # so add the extra bits there
        if extra_bits > 0:
            sizes_str = str(extra_bits) + sizes_str

    return sizes_str


def describe(format_str):
    # The BGR666 format is a special case
    if format_str == "V4L2_PIX_FMT_BGR666":
        return describe_bgr666()

    match = v4l2_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    sizes_str = match.group("sizes")
    x_str = match.group("x")

    # Exception for "A/XBGR" which should really be "BGRA/X"
    if components_str == "ABGR":
        components_str = "BGRA"
    elif components_str == "XBGR":
        components_str = "BGRX"

    # Array formats have "32" or "24" as bits specification
    array_format = sizes_str == "32" or sizes_str == "24"

    sizes_str = normalize_sizes_str(components_str, sizes_str)
    components, sizes = util.parse_components_with_separate_sizes(components_str + sizes_str)
    bits = util.expand_components(components, sizes)

    if array_format:
        memory = util.split_bytes(bits)
    else:
        if x_str is None:
            memory = util.native_to_memory_le(bits)
        else:
            memory = util.native_to_memory_be(bits)

    return FormatDescription(
        data_type = "UNORM",
        native = None,
        memory_le = memory,
        memory_be = memory)

def formats():
    return v4l2_formats

def document():
    return util.read_documentation("v4l2.md")
