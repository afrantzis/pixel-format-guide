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

from .pfgtest import TestCase, R, G, B, A, X, Rn, Gn, Bn, An

class SkiaTest(TestCase):
    def test_32bpp_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "kRGBA_8888_SkColorType",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = None)

    def test_16bpp_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "kRGB_565_SkColorType",
            native = None,
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = None)

        self.assertFormatMatchesUnorm(
            format_str = "kARGB_4444_SkColorType",
            native = None,
            memory_le = [B(3, 0) + A(3, 0), R(3, 0) + G(3, 0)],
            memory_be = None)

    def test_8bpp_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "kAlpha_8_SkColorType",
            native = None,
            memory_le = [A(7, 0)],
            memory_be = None)

    def test_float_formats(self):
        self.assertFormatMatches(
            format_str = "kRGBA_F16_SkColorType",
            data_type = "SFLOAT",
            native = None,
            memory_le = [
                R(7, 0), R(15, 8),
                G(7, 0), G(15, 8),
                B(7, 0), B(15, 8),
                A(7, 0), A(15, 8)],
            memory_be = None)

    def test_unknown_formats(self):
        self.assertFormatIsUnknown("kRGBA_4444_SkColorType")

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "skia",
            everywhere = [],
            little_endian = ["kRGB_565_SkColorType"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "skia",
            everywhere = [],
            little_endian = ["kBGRA_8888_SkColorType"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "PIXMAN_x8b8g8r8",
            family_str = "skia",
            everywhere = [],
            little_endian = ["kRGBA_8888_SkColorType"],
            big_endian = [],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("skia")
