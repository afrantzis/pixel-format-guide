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

import os

subscripts = ['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉']

def subscript(n):
    ret = ""
    digits = str(n)
    for d in digits:
        ret = ret + subscripts[int(d)]
    return ret

def split_bits(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def split_bytes(s):
    return split_bits(s, 8)

def native_to_memory_be(native):
    return split_bytes(native)

def native_to_memory_le(native):
    byte_list = split_bytes(native)
    return [b for b in reversed(byte_list)]

def split_bytes_le(components, n):
    ret = []
    s = split_bits(components, 8 * n)
    for w in s:
        ret = ret + native_to_memory_le(w)
    return ret

def split_bytes_be(components, n):
    ret = []
    s = split_bits(components, 8 * n)
    for w in s:
        ret = ret + native_to_memory_be(w)
    return ret

def component_bits(component, msb, lsb):
    if component == '': return []
    return [component + subscript(i) for i in reversed(range(lsb, msb + 1))]

# Parse component strings of the form: R8G8B8A8
def parse_components_with_mixed_sizes(component_str):
    components = []
    sizes = []

    for c in component_str:
        if c.isdigit():
            sizes[-1] = sizes[-1] * 10 + int(c)
        else:
            components.append(c)
            sizes.append(0)

    return components, sizes

# Parse component strings of the form: RGBA8888
def parse_components_with_separate_sizes(component_str, group_16=False):
    components = []
    sizes = []

    for c in component_str:
        if c.isdigit():
            if c == '0':
                sizes[-1] = sizes[-1] * 10
            elif group_16 and c == '6' and len(sizes) > 0 and sizes[-1] == 1:
                sizes[-1] = sizes[-1] * 10 + 6
            else:
                sizes.append(int(c))
        else:
            components.append(c)

    return components, sizes

def expand_components(components, sizes, default_size=8):
    normalized_sizes = sizes
    normalized_sizes.extend([default_size] * (len(components) - len(normalized_sizes)))

    ret = []

    for c,s in zip(components, normalized_sizes):
        ret = ret + component_bits(c, s - 1, 0)

    return ret

def pixel_bits(bits, i):
    if i == 0:
        return bits

    ret = []
    for b in bits:
        component = ''.join((c for c in b if c not in subscripts))
        ret.append(b.replace(component, "(" + component + "+%d)" % i))

    return ret

def native_to_memory_byte_le(bits):
    byte = []

    pixels_per_byte = 8 // len(bits)
    for i in range(0, pixels_per_byte):
        byte = pixel_bits(bits, i) + byte

    return [byte]

def native_to_memory_byte_be(bits):
    byte = []

    pixels_per_byte = 8 // len(bits)
    for i in range(0, pixels_per_byte):
        byte = byte + pixel_bits(bits, i)

    return [byte]

def read_documentation(docfile):
    here_path = os.path.realpath(os.path.dirname(__file__))
    doc_path = os.path.join(here_path, "..", "docs", docfile)
    doc = ""

    with open(doc_path) as f:
        doc = f.read()

    return doc
