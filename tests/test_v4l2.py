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

from . import pfgtest

class V4L2Test(pfgtest.TestCase):
    def test_packed_formats_le(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB332",
            native = None,
            memory_le = ["R" * 3 + "G" * 3 + "B" * 2],
            memory_be = ["R" * 3 + "G" * 3 + "B" * 2])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB565",
            native = None,
            memory_le = ["G" * 3 + "B" * 5, "R" * 5 + "G" * 3],
            memory_be = ["G" * 3 + "B" * 5, "R" * 5 + "G" * 3])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XRGB555",
            native = None,
            memory_le = ["G" * 3 + "B" * 5, "X" + "R" * 5 + "G" * 2],
            memory_be = ["G" * 3 + "B" * 5, "X" + "R" * 5 + "G" * 2])

    def test_packed_formats_be(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_RGB565X",
            native = None,
            memory_le = ["R" * 5 + "G" * 3, "G" * 3 + "B" * 5],
            memory_be = ["R" * 5 + "G" * 3, "G" * 3 + "B" * 5])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XRGB555X",
            native = None,
            memory_le = ["X" + "R" * 5 + "G" * 2, "G" * 3 + "B" * 5],
            memory_be = ["X" + "R" * 5 + "G" * 2, "G" * 3 + "B" * 5])

    def test_array_formats(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_BGR24",
            native = None,
            memory_le = ["B" * 8, "G" * 8, "R" * 8],
            memory_be = ["B" * 8, "G" * 8, "R" * 8])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_ARGB32",
            native = None,
            memory_le = ["A" * 8, "R" * 8, "G" * 8, "B" * 8],
            memory_be = ["A" * 8, "R" * 8, "G" * 8, "B" * 8])

    def test_format_exceptions(self):
        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_ABGR32",
            native = None,
            memory_le = ["B" * 8, "G" * 8, "R" * 8, "A" * 8],
            memory_be = ["B" * 8, "G" * 8, "R" * 8, "A" * 8])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_XBGR32",
            native = None,
            memory_le = ["B" * 8, "G" * 8, "R" * 8, "X" * 8],
            memory_be = ["B" * 8, "G" * 8, "R" * 8, "X" * 8])

        self.assertFormatMatches(
            format_str = "V4L2_PIX_FMT_BGR666",
            native = None,
            memory_le = ["B" * 6 + "G" * 2, "G" * 4 + "R" * 4, "R" * 2 + "X" * 6],
            memory_be = ["B" * 6 + "G" * 2, "G" * 4 + "R" * 4, "R" * 2 + "X" * 6])

    def test_documentation(self):
        self.assertHasDocumentationFor("v4l2")
