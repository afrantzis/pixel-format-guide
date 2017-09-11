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

opengl_re = re.compile("GL_(?P<components>\w+)\WGL_(?P<data_type>[A-Z_]+)(?P<sizes>[0-9_]+)?(?P<rev>REV)?")

data_type_to_size_dict = {
    "UNSIGNED_BYTE" : 8,
    "BYTE" : 8,
    "UNSIGNED_SHORT" : 16,
    "SHORT" : 16,
    "UNSIGNED_INT" : 32,
    "INT" : 32,
    "HALF_FLOAT": 16,
    "FLOAT" : 32
    }

def data_type_to_size(data_type):
    return data_type_to_size_dict.get(data_type, 0)

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
    sizes_str = match.group("sizes")
    sizes_str = sizes_str.strip("_ ") if sizes_str else None
    rev_str = match.group("rev")

    if rev_str is not None:
        components_str = components_str[::-1]

    if sizes_str is None:
        sizes = [data_type_to_size(data_type_str)] * len(components_str)
    else:
        sizes = [int(s) for s in sizes_str.split("_")]

    bits = util.expand_components(components_str, sizes)

    packed = sizes_str is not None

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
    return util.read_documentation("opengl.md")

