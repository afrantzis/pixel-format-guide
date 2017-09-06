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

def components_to_memory(components):
    return util.split_bytes(components)

def describe(format_str):
    match = vk_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components = util.parse_components_with_mixed_sizes(components_str)
    packed = match.group("pack") is not None

    if packed:
        return FormatDescription(
            native = components,
            memory_le = util.native_to_memory_le(components),
            memory_be = util.native_to_memory_be(components))
    else:
        return FormatDescription(
            native = None,
            memory_le = components_to_memory(components),
            memory_be = components_to_memory(components))

def document():
    return util.read_documentation("vulkan.md")
