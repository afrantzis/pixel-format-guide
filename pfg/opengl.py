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
import itertools

opengl_re = re.compile("GL_(?P<components>\w+)\WGL_(?P<data_type>[A-Z_]+)(?P<bits>[0-9_]+)?(?P<rev>REV)?")

data_type_to_bits_dict = {
    "UNSIGNED_BYTE" : 8,
    "BYTE" : 8,
    "UNSIGNED_SHORT" : 16,
    "SHORT" : 16,
    "UNSIGNED_INT" : 32,
    "INT" : 32,
    "HALF_FLOAT": 16,
    "FLOAT" : 32
    }

def components_to_memory(components):
    return util.split_bytes(components)

def mix_components_and_bits(components, bits):
    bits_as_str = [str(b) for b in bits]
    return "".join(itertools.chain.from_iterable(zip(components, bits_as_str)))

def data_type_to_bits(data_type):
    return data_type_to_bits_dict.get(data_type, 0)

def normalize_components(components_str):
    ret = components_str.replace("_INTEGER", "")
    if ret == "RED":
        ret = "R"
    elif ret == "GREEN":
        ret = "G"
    elif ret == "BLUE":
        ret = "B"

    return ret

def describe(format_str):
    match = opengl_re.match(format_str)

    if not match:
        return None

    components_str = normalize_components(match.group("components"))
    data_type_str = match.group("data_type").strip("_ ")
    bits_str = match.group("bits")
    bits_str = bits_str.strip("_ ") if bits_str else None
    rev_str = match.group("rev")

    if rev_str is not None:
        components_str = components_str[::-1]

    if bits_str is None:
        component_bits = [data_type_to_bits(data_type_str)] * len(components_str)
    else:
        component_bits = bits_str.split("_")

    mixed_components_str = mix_components_and_bits(components_str, component_bits)
    components = util.parse_components_with_mixed_sizes(mixed_components_str)

    packed = bits_str is not None

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
    return util.read_documentation("opengl.md")

