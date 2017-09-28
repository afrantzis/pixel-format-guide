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

import sys
import argparse
from . import commands
from . import util

def find_all(s, m):
    return [i for i, c in enumerate(s) if c == m]

def remove_subscripts(s):
    return "".join((c for c in s if c not in util.subscripts))

def print_indented(indent, s):
    print(" " * indent + s)

def print_memory(text, memory, hide_bit_indices):
    memory_str = " ".join(("".join(b) for b in memory))
    if hide_bit_indices:
        memory_str = remove_subscripts(memory_str)
    header_byte = [" "] * len(memory_str)
    header_ml = [" "] * len(memory_str)

    spaces = find_all(memory_str, " ")

    header_byte[0] = "0";
    header_ml[0] = "M";

    for i, p in enumerate(spaces):
        header_byte[p + 1] = str(i + 1)
        header_ml[p - 1] = "L";
        header_ml[p + 1] = "M";

    header_ml[-1] = "L";

    print(text + "".join(header_byte).strip())
    print_indented(len(text), "".join(header_ml).strip())
    print_indented(len(text), memory_str.strip())

def print_native(text, native, hide_bit_indices):
    native_str = "".join(native)
    if hide_bit_indices:
        native_str = remove_subscripts(native_str)
    print(text + "M" + " " * (len(native_str) - 2) + "L")
    print_indented(len(text), native_str);

def describe(args):
    description = commands.describe(args.format)
    if description:
        print("Format:               %s" % args.format)
        if description.native:
            print("Described as:         Native %d-bit type" % len(description.native))
            print_native("Native type:          ", description.native, args.hide_bit_indices)
        else:
            print("Described as:         Bytes in memory")
        print_memory("Memory little-endian: ", description.memory_le, args.hide_bit_indices)
        print_memory("Memory big-endian:    ", description.memory_be, args.hide_bit_indices)
    else:
        print("Unknown pixel format '%s'" % args.format)

def document(args):
    doc = commands.document(args.family)
    if doc:
        print(doc)
    else:
        print("Unknown or undocumented pixel format family '%s'" % args.family)

def find_compatible(args):
    compatibility = commands.find_compatible(args.format, args.family)
    if compatibility:
        print("Format: %s" % args.format)
        print("Is compatible on all systems with:")
        for f in compatibility.everywhere:
            print_indented(8, f)
        print("Is compatible on little-endian systems with:")
        for f in compatibility.little_endian:
            print_indented(8, f)
        print("Is compatible on big-endian systems with:")
        for f in compatibility.big_endian:
            print_indented(8, f)
    else:
        print("Unknown pixel format '%s' or family '%s'" % (args.format, args.family))

def main(argv):
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()

    parser_describe = subparsers.add_parser(
        "describe", description="Describe a pixel format")
    parser_describe.add_argument("format")
    parser_describe.add_argument(
        "--hide-bit-indices", action='store_true', help="Hide the indices of component bits")
    parser_describe.set_defaults(func=describe)

    parser_document = subparsers.add_parser(
        "document", description="Display pixel format family documentation")
    parser_document.add_argument("family")
    parser_document.set_defaults(func=document)

    parser_find_compatible = subparsers.add_parser(
        "find-compatible",
        description="Find all formats from a family that are compatible with the given format.")
    parser_find_compatible.add_argument("format")
    parser_find_compatible.add_argument("family")
    parser_find_compatible.set_defaults(func=find_compatible)

    args = parser.parse_args(argv[1:])

    args.func(args)
