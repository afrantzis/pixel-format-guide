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

wl_drm_re = re.compile("WL_DRM_FORMAT_(?P<components>.*)")

wl_drm_formats = [
    "WL_DRM_FORMAT_C8",
    "WL_DRM_FORMAT_RGB332",
    "WL_DRM_FORMAT_BGR233",
    "WL_DRM_FORMAT_XRGB4444",
    "WL_DRM_FORMAT_XBGR4444",
    "WL_DRM_FORMAT_RGBX4444",
    "WL_DRM_FORMAT_BGRX4444",
    "WL_DRM_FORMAT_ARGB4444",
    "WL_DRM_FORMAT_ABGR4444",
    "WL_DRM_FORMAT_RGBA4444",
    "WL_DRM_FORMAT_BGRA4444",
    "WL_DRM_FORMAT_XRGB1555",
    "WL_DRM_FORMAT_XBGR1555",
    "WL_DRM_FORMAT_RGBX5551",
    "WL_DRM_FORMAT_BGRX5551",
    "WL_DRM_FORMAT_ARGB1555",
    "WL_DRM_FORMAT_ABGR1555",
    "WL_DRM_FORMAT_RGBA5551",
    "WL_DRM_FORMAT_BGRA5551",
    "WL_DRM_FORMAT_RGB565",
    "WL_DRM_FORMAT_BGR565",
    "WL_DRM_FORMAT_RGB888",
    "WL_DRM_FORMAT_BGR888",
    "WL_DRM_FORMAT_XRGB8888",
    "WL_DRM_FORMAT_XBGR8888",
    "WL_DRM_FORMAT_RGBX8888",
    "WL_DRM_FORMAT_BGRX8888",
    "WL_DRM_FORMAT_ARGB8888",
    "WL_DRM_FORMAT_ABGR8888",
    "WL_DRM_FORMAT_RGBA8888",
    "WL_DRM_FORMAT_BGRA8888",
    "WL_DRM_FORMAT_XRGB2101010",
    "WL_DRM_FORMAT_XBGR2101010",
    "WL_DRM_FORMAT_RGBX1010102",
    "WL_DRM_FORMAT_BGRX1010102",
    "WL_DRM_FORMAT_ARGB2101010",
    "WL_DRM_FORMAT_ABGR2101010",
    "WL_DRM_FORMAT_RGBA1010102",
    "WL_DRM_FORMAT_BGRA1010102",
    "WL_DRM_FORMAT_YUYV",
    "WL_DRM_FORMAT_YVYU",
    "WL_DRM_FORMAT_UYVY",
    "WL_DRM_FORMAT_VYUY",
    "WL_DRM_FORMAT_AYUV",
    ]

def rgba_bits_to_memory(components):
    return util.native_to_memory_le(components)

def yuv_bits_to_memory(components):
    return util.split_bytes(components)

def describe(format_str):
    if not format_str.startswith("WL_DRM_FORMAT") or format_str not in formats():
        return None

    match = wl_drm_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_separate_sizes(components_str)
    bits = util.expand_components(components, sizes)

    if "Y" in components_str:
        memory = yuv_bits_to_memory(bits)
    else:
        memory = rgba_bits_to_memory(bits)

    return FormatDescription(
            data_type = "UNORM",
            native = None,
            memory_le = memory,
            memory_be = memory)

def formats():
    return wl_drm_formats

def document():
    return util.read_documentation("wayland_drm.md")
