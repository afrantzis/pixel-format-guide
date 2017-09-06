from .format_description import FormatDescription
from . import util
import re

wl_drm_re = re.compile("WL_DRM_FORMAT_(?P<components>.*)")

def rgba_components_to_memory(components):
    return util.native_to_memory_le(components)

def yuv_components_to_memory(components):
    return util.split_every_eight_chars(components)

def describe(format_str):
    match = wl_drm_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components = util.parse_components_with_separate_sizes(components_str)

    if "Y" in components_str:
        memory = yuv_components_to_memory(components)
    else:
        memory = rgba_components_to_memory(components)

    return FormatDescription(
            native = None,
            memory_le = memory,
            memory_be = memory)

def document():
    return util.read_documentation("wayland_drm.md")
