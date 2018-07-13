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

directfb_re = re.compile("DSPF_(?P<components>[RGBAi]+)(?P<sizes>\d+)?(?P<lsb>_LSB)?")

directfb_formats = [
    "DSPF_ARGB1555",
    "DSPF_RGB16",
    "DSPF_RGB24",
    "DSPF_RGB32",
    "DSPF_ARGB",
    "DSPF_A8",
    "DSPF_RGB332",
    "DSPF_AiRGB",
    "DSPF_A1",
    "DSPF_ARGB2554",
    "DSPF_ARGB4444",
    "DSPF_RGBA4444",
    "DSPF_A4",
    "DSPF_ARGB1666",
    "DSPF_ARGB6666",
    "DSPF_RGB18",
    "DSPF_RGB444",
    "DSPF_RGB555",
    "DSPF_BGR555",
    "DSPF_RGBA5551",
    "DSPF_ARGB8565",
    "DSPF_A1_LSB",
    "DSPF_ABGR",
    ]

def normalize_components_sizes(components_str, sizes_str):
    # A sizes_str of 16, 18, 24 or 32 denotes the total size divided equally
    # (or as close to equally as possible) between the components.
    sizes_str = {
        "16" : "565",
        "18" : "666",
        "24" : "888",
        "32" : "8888",
        None : "8888"
    }.get(sizes_str, sizes_str)

    components_str = components_str.replace("i", "")

    # X bits (don't care) are implicitly described. Make them explicit.
    total_size = sum((int(s) for s in sizes_str))

    if total_size > 8 and total_size < 16:
        components_str = "X" + components_str
        sizes_str = str(16 - total_size) + sizes_str
    elif total_size > 16 and total_size < 24:
        components_str = "X" + components_str
        sizes_str = str(24 - total_size) + sizes_str

    if len(sizes_str) > len(components_str):
        components_str = "X" + components_str

    return components_str, sizes_str

def describe(format_str):
    if not format_str.startswith("DSPF") or format_str not in formats():
        return None

    match = directfb_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    sizes_str = match.group("sizes")
    lsb_str = match.group("lsb")

    components_str, sizes_str = normalize_components_sizes(components_str, sizes_str)

    components, sizes = util.parse_components_with_separate_sizes(components_str + sizes_str)
    bits = util.expand_components(components, sizes)

    if len(bits) >= 8:
        memory_le = util.native_to_memory_le(bits)
        memory_be = util.native_to_memory_be(bits)
    else:
        if lsb_str is None:
            memory_le = memory_be = util.native_to_memory_byte_be(bits)
        else:
            memory_le = memory_be = util.native_to_memory_byte_le(bits)

    return FormatDescription(
            data_type = "UNORM",
            native = bits,
            memory_le = memory_le,
            memory_be = memory_be)

def formats():
    return directfb_formats

def document():
    return util.read_documentation("directfb.md")
