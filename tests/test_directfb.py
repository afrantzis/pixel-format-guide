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

from .pfgtest import TestCase, R, G, B, A, X, An

class DirectFBTest(TestCase):
    def test_32bit_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_ABGR",
            native = A(7, 0) + B(7, 0) + G(7, 0) + R(7, 0),
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = [A(7, 0), B(7, 0), G(7, 0), R(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_AiRGB",
            native = A(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB32",
            native = X(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), X(7, 0)],
            memory_be = [X(7, 0), R(7, 0), G(7, 0), B(7, 0)])

    def test_24bit_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB24",
            native = R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_ARGB8565",
            native = A(7, 0) + R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3), A(7, 0)],
            memory_be = [A(7, 0), R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB18",
            native = X(5, 0) + R(5, 0) + G(5, 0) + B(5, 0),
            memory_le = [G(1, 0) + B(5, 0), R(3, 0) + G(5, 2), X(5, 0) + R(5, 4)],
            memory_be = [X(5, 0) + R(5, 4), R(3, 0) + G(5, 2), G(1, 0) + B(5, 0)])

    def test_16bit_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB16",
            native = R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_ARGB1555",
            native = A(0, 0) + R(4, 0) + G(4, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), A(0, 0) + R(4, 0) + G(4, 3)],
            memory_be = [A(0, 0) + R(4, 0) + G(4, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB555",
            native = X(0, 0) + R(4, 0) + G(4, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), X(0, 0) + R(4, 0) + G(4, 3)],
            memory_be = [X(0, 0) + R(4, 0) + G(4, 3), G(2, 0) + B(4, 0)])

    def test_8bit_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_A8",
            native = A(7, 0),
            memory_le = [A(7, 0)],
            memory_be = [A(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_RGB332",
            native = R(2, 0) + G(2, 0) + B(1, 0),
            memory_le = [R(2, 0) + G(2, 0) + B(1, 0)],
            memory_be = [R(2, 0) + G(2, 0) + B(1, 0)])

    def test_4bit_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_A4",
            native = A(3, 0),
            memory_le = [A(3, 0) + An(1, 3, 0)],
            memory_be = [A(3, 0) + An(1, 3, 0)])

    def test_1bpp_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "DSPF_A1",
            native = A(0, 0),
            memory_le = [
                A(0, 0) + An(1, 0, 0) + An(2, 0, 0) + An(3, 0, 0) +
                An(4, 0, 0) + An(5, 0, 0) + An(6, 0, 0) + An(7, 0, 0)],
            memory_be = [
                A(0, 0) + An(1, 0, 0) + An(2, 0, 0) + An(3, 0, 0) +
                An(4, 0, 0) + An(5, 0, 0) + An(6, 0, 0) + An(7, 0, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "DSPF_A1_LSB",
            native = A(0, 0),
            memory_le = [
                An(7, 0, 0) + An(6, 0, 0) + An(5, 0, 0) + An(4, 0, 0) +
                An(3, 0, 0) + An(2, 0, 0) + An(1, 0, 0) + A(0, 0)],
            memory_be = [
                An(7, 0, 0) + An(6, 0, 0) + An(5, 0, 0) + An(4, 0, 0) +
                An(3, 0, 0) + An(2, 0, 0) + An(1, 0, 0) + A(0, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "directfb",
            everywhere = ["DSPF_RGB16"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "directfb",
            everywhere = [],
            little_endian = ["DSPF_ARGB", "DSPF_AiRGB"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "directfb",
            everywhere = [],
            little_endian = ["DSPF_ARGB", "DSPF_AiRGB", "DSPF_RGB32"],
            big_endian = [],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("directfb")
