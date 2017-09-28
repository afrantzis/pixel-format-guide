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

from .pfgtest import TestCase, R, G, B, A, X

class V4L2Test(TestCase):
    def test_packed_formats_le(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB332",
            native = None,
            memory_le = [R(2, 0) + G(2, 0) + B(1, 0)],
            memory_be = [R(2, 0) + G(2, 0) + B(1, 0)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB565",
            native = None,
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XRGB555",
            native = None,
            memory_le = [G(2, 0) + B(4, 0), X(0, 0) + R(4, 0) + G(4, 3)],
            memory_be = [G(2, 0) + B(4, 0), X(0, 0) + R(4, 0) + G(4, 3)])

    def test_packed_formats_be(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB565X",
            native = None,
            memory_le = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XRGB555X",
            native = None,
            memory_le = [X(0, 0) + R(4, 0) + G(4, 3), G(2, 0) + B(4, 0)],
            memory_be = [X(0, 0) + R(4, 0) + G(4, 3), G(2, 0) + B(4, 0)])

    def test_array_formats(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_BGR24",
            native = None,
            memory_le = [B(7, 0), G(7, 0), R(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_ARGB32",
            native = None,
            memory_le = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)],
            memory_be = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)])

    def test_format_exceptions(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_ABGR32",
            native = None,
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XBGR32",
            native = None,
            memory_le = [B(7, 0), G(7, 0), R(7, 0), X(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0), X(7, 0)])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_BGR666",
            native = None,
            memory_le = [B(5, 0) + G(5, 4), G(3, 0) + R(5, 2), R(1, 0) + X(5, 0)],
            memory_be = [B(5, 0) + G(5, 4), G(3, 0) + R(5, 2), R(1, 0) + X(5, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "v4l2",
            everywhere = [],
            little_endian = ["V4L2_PIX_FMT_RGB565"],
            big_endian = ["V4L2_PIX_FMT_RGB565X"])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "v4l2",
            everywhere = ["V4L2_PIX_FMT_ABGR32"],
            little_endian = [],
            big_endian = [])

    def test_documentation(self):
        self.assertHasDocumentationFor("v4l2")
