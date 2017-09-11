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

r = "UNORM|SNORM|USCALED|SSCALED|UINT|SINT|SRGB|SFLOAT|UFLOAT"
vk_re = re.compile("VK_FORMAT_(?P<components>.*)_(" + r + ")(?P<pack>_PACK\d+)?")


def describe(format_str):
    match = vk_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_mixed_sizes(components_str)
    bits = util.expand_components(components, sizes)

    packed = match.group("pack") is not None

    if packed:
        return FormatDescription(
            native = bits,
            memory_le = util.native_to_memory_le(bits),
            memory_be = util.native_to_memory_be(bits))
    else:
        return FormatDescription(
            native = None,
            memory_le = util.split_bytes_le(bits, sizes[0] // 8),
            memory_be = util.split_bytes_be(bits, sizes[0] // 8))

def document():
    return util.read_documentation("vulkan.md")
