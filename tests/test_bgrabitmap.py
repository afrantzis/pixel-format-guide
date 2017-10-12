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

class BGRABitmapTest(TestCase):
    def test_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "BGRABITMAP_BGRAPIXEL",
            native = None,
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "BGRABITMAP_RGBAPIXEL",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "bgrabitmap",
            everywhere = ["BGRABITMAP_BGRAPIXEL"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "PIXMAN_x8r8g8b8",
            family_str = "bgrabitmap",
            everywhere = [],
            little_endian = ["BGRABITMAP_BGRAPIXEL"],
            big_endian = [],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("bgrabitmap")
