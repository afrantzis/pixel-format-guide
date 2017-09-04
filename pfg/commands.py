from . import vulkan
from . import wayland_drm

families = [
    vulkan,
    wayland_drm
    ]

def describe(format_str):
    for family in families:
        description = family.describe(format_str)
        if description is not None:
            return description

    return None

def document(family):
    for f in families:
        modname = f.__name__.split(".")[-1]
        if modname == family:
            return f.document()
    return None
