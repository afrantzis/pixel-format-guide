from .format_description import FormatDescription
from . import util
import re

r = "UNORM|SNORM|USCALED|SSCALED|UINT|SINT|SRGB|SFLOAT|UFLOAT"
vk_re = re.compile("VK_FORMAT_(?P<components>.*)_(" + r + ")(?P<pack>_PACK\d+)?")

def components_to_native(components, packed):
    if packed:
        return components
    return None

def components_to_memory_le(components, packed):
    byte_list = util.split_every_eight_chars(components)
    if packed:
        return [b for b in reversed(byte_list)]
    else:
        return byte_list

def components_to_memory_be(components):
    return util.split_every_eight_chars(components)

def describe(format_str):
    match = vk_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components = util.parse_components_with_mixed_sizes(components_str)
    packed = match.group("pack") is not None

    return FormatDescription(
            native = components_to_native(components, packed),
            memory_le = components_to_memory_le(components, packed),
            memory_be = components_to_memory_be(components))

def document():
    return util.read_documentation("vulkan.md")
