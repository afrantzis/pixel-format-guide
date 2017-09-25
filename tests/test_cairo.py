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

class CairoTest(TestCase):
    def test_32bpp_formats(self):
        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_ARGB32",
            native = A(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)])

        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_RGB30",
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

        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_RGB24",
            native = X(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), X(7, 0)],
            memory_be = [X(7, 0), R(7, 0), G(7, 0), B(7, 0)])

    def test_16bpp_formats(self):
        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_RGB16_565",
            native = R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

    def test_8bpp_formats(self):
        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_A8",
            native = A(7, 0),
            memory_le = [A(7, 0)],
            memory_be = [A(7, 0)])

    def test_1bpp_formats(self):
        self.assertFormatMatches(
            format_str = "CAIRO_FORMAT_A1",
            native = A(0, 0),
            memory_le = [
                An(7, 0, 0) + An(6, 0, 0) + An(5, 0, 0) + An(4, 0, 0) +
                An(3, 0, 0) + An(2, 0, 0) + An(1, 0, 0) + A(0, 0)],
            memory_be = [
                A(0, 0) + An(1, 0, 0) + An(2, 0, 0) + An(3, 0, 0) +
                An(4, 0, 0) + An(5, 0, 0) + An(6, 0, 0) + An(7, 0, 0)])

    def test_documentation(self):
        self.assertHasDocumentationFor("cairo")
