import sys
import argparse
from . import commands

def print_indented(indent, s):
    print(" " * indent + s)

def print_memory(text, memory):
    header_byte = (" "*8).join([str(i) for i in range(0, len(memory))])
    header_ml = "M      L " * len(memory)
    memory_str = " ".join(memory)

    print(text + header_byte)
    print_indented(len(text), header_ml)
    print_indented(len(text), memory_str)

def print_native(text, native):
    print(text + "M" + " " * (len(native) - 2) + "L")
    print_indented(len(text), native);

def describe(args):
    description = commands.describe(args.format)
    if description:
        print("Format:               %s" % args.format)
        if description.native:
            print("Described as:         Native %d-bit type" % len(description.native))
            print_native("Native type:          ", description.native)
        else:
            print("Described as:         Bytes in memory")
        print_memory("Memory little-endian: ", description.memory_le)
        print_memory("Memory big-endian:    ", description.memory_be)
    else:
        print("Unknown pixel format '%s'" % args.format)

def document(args):
    doc = commands.document(args.family)
    if doc:
        print(doc)
    else:
        print("Unknown or undocumented pixel format family '%s'" % args.family)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()

    parser_describe = subparsers.add_parser(
        "describe", description="Describe a pixel format")
    parser_describe.add_argument("format")
    parser_describe.set_defaults(func=describe)

    parser_document = subparsers.add_parser(
        "document", description="Display pixel format family documentation")
    parser_document.add_argument("family")
    parser_document.set_defaults(func=document)

    args = parser.parse_args(argv[1:])

    args.func(args)
