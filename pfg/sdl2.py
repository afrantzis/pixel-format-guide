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

sdl2_re = re.compile("SDL_PIXELFORMAT_(?P<components>[RGBAX]+)(?P<sizes>\d+)")

def rgba_components_to_memory(components):
    return util.native_to_memory_le(components)

def yuv_components_to_memory(components):
    return util.split_bytes(components)

def describe(format_str):
    match = sdl2_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    sizes_str = match.group("sizes")

    # Size of 24 or 32 denotes a byte array format, otherwise it's a packed format
    if sizes_str == "24" or sizes_str == "32":
        components, sizes = util.parse_components_with_separate_sizes(components_str)
        bits = util.expand_components(components, sizes)
        return FormatDescription(
                native = None,
                memory_le = util.split_bytes(bits),
                memory_be = util.split_bytes(bits))
    else:
        components, sizes = util.parse_components_with_separate_sizes(components_str + sizes_str)
        bits = util.expand_components(components, sizes)
        return FormatDescription(
                native = bits,
                memory_le = util.native_to_memory_le(bits),
                memory_be = util.native_to_memory_be(bits))

def document():
    return util.read_documentation("sdl2.md")
