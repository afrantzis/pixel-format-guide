from .format_description import FormatDescription
from . import util
import re

r = "UNORM|SNORM|USCALED|SSCALED|UINT|SINT|SRGB|SFLOAT|UFLOAT"
vk_re = re.compile("VK_FORMAT_(?P<components>.*)_(" + r + ")(?P<pack>_PACK\d+)?")

def components_to_memory(components):
    return util.split_every_eight_chars(components)

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
