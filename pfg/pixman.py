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

pixman_re = re.compile("PIXMAN_(?P<components>(?:[argbxcg][0-9]+)+)")

pixman_formats = [
    # 32-bit
    "PIXMAN_a8r8g8b8",
    "PIXMAN_x8r8g8b8",
    "PIXMAN_a8b8g8r8",
    "PIXMAN_x8b8g8r8",
    "PIXMAN_b8g8r8a8",
    "PIXMAN_b8g8r8x8",
    "PIXMAN_r8g8b8a8",
    "PIXMAN_r8g8b8x8",
    "PIXMAN_x14r6g6b6",
    "PIXMAN_x2r10g10b10",
    "PIXMAN_a2r10g10b10",
    "PIXMAN_x2b10g10r10",
    "PIXMAN_a2b10g10r10",
    "PIXMAN_a8r8g8b8_sRGB",
    # 24-bit
    "PIXMAN_r8g8b8",
    "PIXMAN_b8g8r8",
    # 16-bit
    "PIXMAN_r5g6b5",
    "PIXMAN_b5g6r5",
    "PIXMAN_a1r5g5b5",
    "PIXMAN_x1r5g5b5",
    "PIXMAN_a1b5g5r5",
    "PIXMAN_x1b5g5r5",
    "PIXMAN_a4r4g4b4",
    "PIXMAN_x4r4g4b4",
    "PIXMAN_a4b4g4r4",
    "PIXMAN_x4b4g4r4",
    # 8-bit
    "PIXMAN_a8",
    "PIXMAN_r3g3b2",
    "PIXMAN_b2g3r3",
    "PIXMAN_a2r2g2b2",
    "PIXMAN_a2b2g2r2",
    "PIXMAN_c8",
    "PIXMAN_g8",
    "PIXMAN_x4a4",
    "PIXMAN_x4c4",
    "PIXMAN_x4g4",
    # 4-bit
    "PIXMAN_a4",
    "PIXMAN_r1g2b1",
    "PIXMAN_b1g2r1",
    "PIXMAN_a1r1g1b1",
    "PIXMAN_a1b1g1r1",
    "PIXMAN_c4",
    "PIXMAN_g4",
    # 1-bit
    "PIXMAN_a1",
    "PIXMAN_g1"
    ]

def describe(format_str):
    if not format_str.startswith("PIXMAN_") or format_str not in formats():
        return None

    match = pixman_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components").upper()
    components, sizes = util.parse_components_with_mixed_sizes(components_str)
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
    return pixman_formats

def document():
    return util.read_documentation("pixman.md")
