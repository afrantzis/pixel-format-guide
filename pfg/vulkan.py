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

r = "UNORM|SNORM|USCALED|SSCALED|UINT|SINT|SRGB|SFLOAT|UFLOAT"
vk_re = re.compile("VK_FORMAT_(?P<components>.*)_(" + r + ")(?P<pack>_PACK\d+)?")

def gen_vk_formats(template, spec):
    return [t % s for t in template for s in spec]

def describe(format_str):
    match = vk_re.match(format_str)

    if not match:
        return None

    components_str = match.group("components")
    components, sizes = util.parse_components_with_mixed_sizes(components_str)
    bits = util.expand_components(components, sizes)

    packed = match.group("pack") is not None

    if packed:
        return FormatDescription(
            native = bits,
            memory_le = util.native_to_memory_le(bits),
            memory_be = util.native_to_memory_be(bits))
    else:
        return FormatDescription(
            native = None,
            memory_le = util.split_bytes_le(bits, sizes[0] // 8),
            memory_be = util.split_bytes_be(bits, sizes[0] // 8))

def formats():
    formats = [
        "VK_FORMAT_R4G4_UNORM_PACK8",
        "VK_FORMAT_R4G4B4A4_UNORM_PACK16",
        "VK_FORMAT_B4G4R4A4_UNORM_PACK16",
        "VK_FORMAT_R5G6B5_UNORM_PACK16",
        "VK_FORMAT_B5G6R5_UNORM_PACK16",
        "VK_FORMAT_R5G5B5A1_UNORM_PACK16",
        "VK_FORMAT_B5G5R5A1_UNORM_PACK16",
        "VK_FORMAT_A1R5G5B5_UNORM_PACK16",
        "VK_FORMAT_B10G11R11_UFLOAT_PACK32",
        "VK_FORMAT_E5B9G9R9_UFLOAT_PACK32",
        "VK_FORMAT_D16_UNORM",
        "VK_FORMAT_X8_D24_UNORM_PACK32",
        "VK_FORMAT_D32_SFLOAT",
        "VK_FORMAT_S8_UINT",
        ]

    formats += gen_vk_formats(
        [
            "VK_FORMAT_R8_%s",
            "VK_FORMAT_R8G8_%s",
            "VK_FORMAT_R8G8B8_%s",
            "VK_FORMAT_B8G8R8_%s",
            "VK_FORMAT_R8G8B8A8_%s",
            "VK_FORMAT_B8G8R8A8_%s",
            "VK_FORMAT_A8B8G8R8_%s_PACK32",
        ],
        ["UNORM", "SNORM", "USCALED", "SSCALED", "UINT", "SINT", "SRGB"])

    formats += gen_vk_formats(
        [
            "VK_FORMAT_A2R10G10B10_%s_PACK32",
            "VK_FORMAT_A2B10G10R10_%s_PACK32",
        ],
        ["UNORM", "SNORM", "USCALED", "SSCALED", "UINT", "SINT"])

    formats += gen_vk_formats(
        [
            "VK_FORMAT_R16_%s",
            "VK_FORMAT_R16G16_%s",
            "VK_FORMAT_R16G16B16_%s",
            "VK_FORMAT_R16G16B16A16_%s",
        ],
        ["UNORM", "SNORM", "USCALED", "SSCALED", "UINT", "SINT", "SFLOAT"])

    formats += gen_vk_formats(
        [
            "VK_FORMAT_R32_%s",
            "VK_FORMAT_R32G32_%s",
            "VK_FORMAT_R32G32B32_%s",
            "VK_FORMAT_R32G32B32A32_%s",
            "VK_FORMAT_R64_%s",
            "VK_FORMAT_R64G64_%s",
            "VK_FORMAT_R64G64B64_%s",
            "VK_FORMAT_R64G64B64A64_%s",
        ],
        ["UINT", "SINT", "SFLOAT"])

    return formats

def document():
    return util.read_documentation("vulkan.md")
