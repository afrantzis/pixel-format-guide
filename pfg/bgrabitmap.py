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

bgrabitmap_re = re.compile("BGRABITMAP_(?P<components>BGRA|RGBA)PIXEL")

bgrabitmap_formats = [
    "BGRABITMAP_BGRAPIXEL",
    "BGRABITMAP_RGBAPIXEL",
    ]

def describe(format_str):
    match = bgrabitmap_re.match(format_str)
    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)
    memory = util.split_bytes(bits)

    return FormatDescription(
        native = None,
        memory_le = memory,
        memory_be = memory)

def formats():
    return bgrabitmap_formats

def document():
    return util.read_documentation("bgrabitmap.md")
