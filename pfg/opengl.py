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

gl_data_type_to_size_dict = {
    "UNSIGNED_BYTE" : 8,
    "BYTE" : 8,
    "UNSIGNED_SHORT" : 16,
    "SHORT" : 16,
    "UNSIGNED_INT" : 32,
    "INT" : 32,
    "HALF_FLOAT": 16,
    "FLOAT" : 32
    }

def gl_data_type_to_size(data_type):
    return gl_data_type_to_size_dict.get(data_type, 0)

def data_type_from_format(format_str):
    if "FLOAT" in format_str:
        dt = "FLOAT"
    elif "INTEGER" in format_str:
        dt = "INT"
    else:
        dt = "NORM"

    if "UNSIGNED" in format_str:
        dt = "U" + dt
    else:
        dt = "S" + dt

    return dt

def normalize_components(components_str):
    ret = components_str.replace("_INTEGER", "")
    if ret == "RED":
        ret = "R"
    elif ret == "GREEN":
        ret = "G"
    elif ret == "BLUE":
        ret = "B"

    return ret

def gen_packed_formats(bits):
    if len(bits) == 4:
        formats = ["GL_RGBA", "GL_BGRA", "GL_RGBA_INTEGER", "GL_BGRA_INTEGER"]
    elif len(bits) == 3:
        formats = ["GL_RGB", "GL_RGB_INTEGER"]

    data_type = {
        8: "UNSIGNED_BYTE",
        16: "UNSIGNED_SHORT",
        32: "UNSIGNED_INT"
        }[sum(bits)]

    types = [
        "GL_" + data_type + "_" + "_".join((str(b) for b in bits)),
        "GL_" + data_type + "_" + "_".join((str(b) for b in reversed(bits))) + "_REV"
        ]

    return [f + "+" + t for f in formats for t in types]

def gen_array_formats(components):
    component = ["".join(components), "".join(components) + "_INTEGER"]
    return ["GL_" + c + "+" + "GL_" + dt for c in component for dt in gl_data_type_to_size_dict]

def describe(format_str):
    if not format_str.startswith("GL_") or format_str not in formats():
        return None

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
        sizes = [gl_data_type_to_size(data_type_str)] * len(components_str)
    else:
        sizes = [int(s) for s in sizes_str.split("_")]

    bits = util.expand_components(components_str, sizes)

    packed = sizes_str is not None

    if packed:
        return FormatDescription(
            data_type = data_type_from_format(format_str),
            native = bits,
            memory_le = util.native_to_memory_le(bits),
            memory_be = util.native_to_memory_be(bits))
    else:
        return FormatDescription(
            data_type = data_type_from_format(format_str),
            native = None,
            memory_le = util.split_bytes_le(bits, sizes[0] // 8),
            memory_be = util.split_bytes_be(bits, sizes[0] // 8))

def formats():
    formats = []

    formats += gen_packed_formats([3, 3, 2])
    formats += gen_packed_formats([5, 6, 5])
    formats += gen_packed_formats([4, 4, 4, 4])
    formats += gen_packed_formats([5, 5, 5, 1])
    formats += gen_packed_formats([8, 8, 8, 8])
    formats += gen_packed_formats([10, 10, 10, 2])

    formats += gen_array_formats(["RED"])
    formats += gen_array_formats(["GREEN"])
    formats += gen_array_formats(["BLUE"])
    formats += gen_array_formats(["R", "G"])
    formats += gen_array_formats(["R", "G", "B"])
    formats += gen_array_formats(["R", "G", "B", "A"])
    formats += gen_array_formats(["B", "G", "R"])
    formats += gen_array_formats(["B", "G", "R", "A"])

    return formats

def document():
    return util.read_documentation("opengl.md")
