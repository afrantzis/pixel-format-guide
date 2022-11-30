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

drm_re = re.compile("DRM_FORMAT_(?P<components>.*)")

drm_formats = [
    "DRM_FORMAT_C8",
    "DRM_FORMAT_R8",
    "DRM_FORMAT_R16",
    "DRM_FORMAT_RG88",
    "DRM_FORMAT_GR88",
    "DRM_FORMAT_RG1616",
    "DRM_FORMAT_GR1616",
    "DRM_FORMAT_RGB332",
    "DRM_FORMAT_BGR233",
    "DRM_FORMAT_XRGB4444",
    "DRM_FORMAT_XBGR4444",
    "DRM_FORMAT_RGBX4444",
    "DRM_FORMAT_BGRX4444",
    "DRM_FORMAT_ARGB4444",
    "DRM_FORMAT_ABGR4444",
    "DRM_FORMAT_RGBA4444",
    "DRM_FORMAT_BGRA4444",
    "DRM_FORMAT_XRGB1555",
    "DRM_FORMAT_XBGR1555",
    "DRM_FORMAT_RGBX5551",
    "DRM_FORMAT_BGRX5551",
    "DRM_FORMAT_ARGB1555",
    "DRM_FORMAT_ABGR1555",
    "DRM_FORMAT_RGBA5551",
    "DRM_FORMAT_BGRA5551",
    "DRM_FORMAT_RGB565",
    "DRM_FORMAT_BGR565",
    "DRM_FORMAT_RGB888",
    "DRM_FORMAT_BGR888",
    "DRM_FORMAT_XRGB8888",
    "DRM_FORMAT_XBGR8888",
    "DRM_FORMAT_RGBX8888",
    "DRM_FORMAT_BGRX8888",
    "DRM_FORMAT_ARGB8888",
    "DRM_FORMAT_ABGR8888",
    "DRM_FORMAT_RGBA8888",
    "DRM_FORMAT_BGRA8888",
    "DRM_FORMAT_XRGB2101010",
    "DRM_FORMAT_XBGR2101010",
    "DRM_FORMAT_RGBX1010102",
    "DRM_FORMAT_BGRX1010102",
    "DRM_FORMAT_ARGB2101010",
    "DRM_FORMAT_ABGR2101010",
    "DRM_FORMAT_RGBA1010102",
    "DRM_FORMAT_BGRA1010102",
    "DRM_FORMAT_XRGB16161616",
    "DRM_FORMAT_XBGR16161616",
    "DRM_FORMAT_ARGB16161616",
    "DRM_FORMAT_ABGR16161616",
    "DRM_FORMAT_YUYV",
    "DRM_FORMAT_YVYU",
    "DRM_FORMAT_UYVY",
    "DRM_FORMAT_VYUY",
    "DRM_FORMAT_AYUV",
    ]

def rgba_bits_to_memory(components):
    return util.native_to_memory_le(components)

def yuv_bits_to_memory(components):
    return util.split_bytes(components)

def describe(format_str):
    if not format_str.startswith("DRM_FORMAT") or format_str not in formats():
        return None

    match = drm_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_separate_sizes(
        components_str, group_16=True)
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
    return drm_formats

def document():
    return util.read_documentation("drm.md")
