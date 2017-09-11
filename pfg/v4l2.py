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

v4l2_re = re.compile("V4L2_PIX_FMT_(?P<components>[RGBAX]+)(?P<bits>\d+)(?P<x>X)?")

def describe_bgr666():
    memory = ["BBBBBBGG", "GGGGRRRR", "RRXXXXXX"]
    return FormatDescription(
        native = None,
        memory_le = memory,
        memory_be = memory)

# Normalize bits string to contain bit values for all components
def normalize_bits_str(components_str, bits_str):

    if bits_str == "32":
        bits_str = "8888";
    elif bits_str == "24":
        bits_str = "888";

    # The size of the A/X component is not explicitly specified; we need to
    # infer it from the components, the specified bits and the size of the
    # native type (which is always a multiple of 8 bits)
    if "X" in components_str or "A" in components_str:
        specified_bits = sum([int(i) for i in bits_str])
        format_bits = int(math.ceil(specified_bits / 8) * 8)
        extra_bits = format_bits - specified_bits
        # The A/X component is always at the beginning of the component_str
        # so add the extra bits there
        if extra_bits > 0:
            bits_str = str(extra_bits) + bits_str

    return bits_str


def describe(format_str):
    # The BGR666 format is a special case
    if format_str == "V4L2_PIX_FMT_BGR666":
        return describe_bgr666()

    match = v4l2_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    bits_str = match.group("bits")
    x_str = match.group("x")

    # Exception for "A/XBGR" which should really be "BGRA/X"
    if components_str == "ABGR":
        components_str = "BGRA"
    elif components_str == "XBGR":
        components_str = "BGRX"

    # Array formats have "32" or "24" as bits specification
    array_format = bits_str == "32" or bits_str == "24"

    bits_str = normalize_bits_str(components_str, bits_str)
    components = util.parse_components_with_separate_sizes(components_str + bits_str)

    if array_format:
        memory = util.split_bytes(components)
    else:
        if x_str is None:
            memory = util.native_to_memory_le(components)
        else:
            memory = util.native_to_memory_be(components)

    return FormatDescription(
        native = None,
        memory_le = memory,
        memory_be = memory)

def document():
    return util.read_documentation("v4l2.md")
