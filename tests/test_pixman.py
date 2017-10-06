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

class PixmanTest(TestCase):
    def test_32bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_b8g8r8a8",
            native = B(7, 0) + G(7, 0) + R(7, 0) + A(7, 0),
            memory_le = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)])

        self.assertFormatMatches(
            format_str = "PIXMAN_x2r10g10b10",
            native = X(1, 0) + R(9, 0) + G(9, 0) + B(9, 0),
            memory_le = [
                B(7, 0),
                G(5, 0) + B(9, 8),
                R(3, 0) + G(9, 6),
                X(1, 0) + R(9, 4)],
            memory_be = [
                X(1, 0) + R(9, 4),
                R(3, 0) + G(9, 6),
                G(5, 0) + B(9, 8),
                B(7, 0)])

    def test_24bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_r8g8b8",
            native = R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0)])

    def test_16bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_r5g6b5",
            native = R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

    def test_8bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_a8",
            native = A(7, 0),
            memory_le = [A(7, 0)],
            memory_be = [A(7, 0)])

        self.assertFormatMatches(
            format_str = "PIXMAN_a2b2g2r2",
            native = A(1, 0) + B(1, 0) + G(1, 0) + R(1, 0),
            memory_le = [A(1, 0) + B(1, 0) + G(1, 0) + R(1, 0)],
            memory_be = [A(1, 0) + B(1, 0) + G(1, 0) + R(1, 0)])

    def test_4bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_a4",
            native = A(3, 0),
            memory_le = [An(1, 3, 0) + A(3, 0)],
            memory_be = [A(3, 0) + An(1, 3, 0)])

        self.assertFormatMatches(
            format_str = "PIXMAN_a1r1g1b1",
            native = A(0, 0) + R(0, 0) + G(0, 0) + B(0, 0),
            memory_le = [
                An(1, 0, 0) + Rn(1, 0, 0) + Gn(1, 0, 0) + Bn(1, 0, 0) +
                A(0, 0) + R(0, 0) + G(0, 0) + B(0, 0)],
            memory_be = [
                A(0, 0) + R(0, 0) + G(0, 0) + B(0, 0) +
                An(1, 0, 0) + Rn(1, 0, 0) + Gn(1, 0, 0) + Bn(1, 0, 0)])

    def test_1bpp_formats(self):
        self.assertFormatMatches(
            format_str = "PIXMAN_a1",
            native = A(0, 0),
            memory_le = [
                An(7, 0, 0) + An(6, 0, 0) + An(5, 0, 0) + An(4, 0, 0) +
                An(3, 0, 0) + An(2, 0, 0) + An(1, 0, 0) + A(0, 0)],
            memory_be = [
                A(0, 0) + An(1, 0, 0) + An(2, 0, 0) + An(3, 0, 0) +
                An(4, 0, 0) + An(5, 0, 0) + An(6, 0, 0) + An(7, 0, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "pixman",
            everywhere = ["PIXMAN_r5g6b5"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "pixman",
            everywhere = [],
            little_endian = [
                "PIXMAN_a8r8g8b8",
                "PIXMAN_a8r8g8b8_sRGB"],
            big_endian = ["PIXMAN_b8g8r8a8"])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "pixman",
            everywhere = [],
            little_endian = [
                "PIXMAN_a8r8g8b8",
                "PIXMAN_a8r8g8b8_sRGB",
                "PIXMAN_x8r8g8b8"],
            big_endian = [
                "PIXMAN_b8g8r8a8",
                "PIXMAN_b8g8r8x8"],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("pixman")
