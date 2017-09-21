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

def describe(format_str):
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
        native = bits,
        memory_le = memory_le,
        memory_be = memory_be)

def document():
    return util.read_documentation("pixman.md")
