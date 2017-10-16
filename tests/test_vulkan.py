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

from .pfgtest import TestCase, R, G, B, A

class VulkanTest(TestCase):
    def test_non_packed_formats(self):
        self.assertFormatMatches(
            format_str = "VK_FORMAT_R8G8B8A8_SRGB",
            data_type = "SRGB",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)])

    def test_non_packed_formats_with_multibyte_components(self):
        self.assertFormatMatchesUnorm(
            format_str = "VK_FORMAT_R16G16_UNORM",
            native = None,
            memory_le = [R(7, 0), R(15, 8), G(7, 0), G(15, 8)],
            memory_be = [R(15, 8), R(7, 0), G(15, 8), G(7, 0)])

    def test_packed_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            native = R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0)+ B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatches(
            format_str = "VK_FORMAT_A2R10G10B10_SSCALED_PACK32",
            data_type = "SSCALED",
            native = A(1, 0) + R(9, 0) + G(9, 0) + B(9, 0),
            memory_le = [
                B(7, 0),
                G(5, 0) + B(9, 8),
                R(3, 0) + G(9, 6),
                A(1, 0) + R(9, 4)],
            memory_be = [
                A(1, 0) + R(9, 4),
                R(3, 0) + G(9, 6),
                G(5, 0) + B(9, 8),
                B(7, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "GL_RGB+GL_UNSIGNED_SHORT_5_6_5",
            family_str = "vulkan",
            everywhere = ["VK_FORMAT_R5G6B5_UNORM_PACK16"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "GL_RGBA+GL_UNSIGNED_BYTE",
            family_str = "vulkan",
            everywhere = ["VK_FORMAT_R8G8B8A8_UNORM"],
            little_endian = ["VK_FORMAT_A8B8G8R8_UNORM_PACK32"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "PIXMAN_x8r8g8b8",
            family_str = "vulkan",
            everywhere = [],
            little_endian = ["VK_FORMAT_B8G8R8A8_UNORM"],
            big_endian = [],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("vulkan")
