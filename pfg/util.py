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

def split_bytes(s):
    return [s[i:i+8] for i in range(0, len(s), 8)]

# Parse component strings of the form: R8G8B8A8
def parse_components_with_mixed_sizes(component_str, default_size=8):
    ret = ""
    current_component = ''
    current_size = 0

    component_size = lambda : current_size if current_size > 0 else default_size

    for c in component_str:
        if c.isdigit():
            current_size = current_size * 10 + int(c)
        else:
            ret = ret + current_component * component_size()
            current_size = 0
            current_component = c

    ret = ret + current_component * component_size()

    return ret

# Parse component strings of the form: RGBA8888
def parse_components_with_separate_sizes(component_str, default_size=8):
    ret = ""
    components = []
    sizes = []

    for c in component_str:
        if c.isdigit():
            if c == '0':
                sizes[-1] = sizes[-1] * 10
            else:
                sizes.append(int(c))
        else:
            components.append(c)

    sizes.extend([default_size] * (len(components) - len(sizes)))

    for c,s in zip(components, sizes):
        ret = ret + c * s

    return ret

def native_to_memory_be(native):
    return split_bytes(native)

def native_to_memory_le(native):
    byte_list = split_bytes(native)
    return [b for b in reversed(byte_list)]

def read_documentation(docfile):
    here_path = os.path.realpath(os.path.dirname(__file__))
    doc_path = os.path.join(here_path, "..", "docs", docfile)
    doc = ""

    with open(doc_path) as f:
        doc = f.read()

    return doc
