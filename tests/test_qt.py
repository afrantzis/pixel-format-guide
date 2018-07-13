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

from .pfgtest import TestCase, R, G, B, A, X, C, Cn

class QtTest(TestCase):
    def test_packed_formats_with_total_size(self):
        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_ARGB32",
            native = A(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [A(7, 0), R(7, 0), G(7, 0), B(7, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_RGB32",
            native = X(7, 0) + R(7, 0) + G(7, 0) + B(7, 0),
            memory_le = [B(7, 0), G(7, 0), R(7, 0), X(7, 0)],
            memory_be = [X(7, 0), R(7, 0), G(7, 0), B(7, 0)])

    def test_packed_formats_with_component_sizes(self):
        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_ARGB8565_Premultiplied",
            native = A(7, 0) + R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), R(4, 0) + G(5, 3), A(7, 0)],
            memory_be = [A(7, 0), R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_RGB555",
            native = X(0, 0) + R(4, 0) + G(4, 0) + B(4, 0),
            memory_le = [G(2, 0) + B(4, 0), X(0, 0) + R(4, 0) + G(4, 3)],
            memory_be = [X(0, 0) + R(4, 0) + G(4, 3), G(2, 0) + B(4, 0)])

    def test_array_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_RGBA8888",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)])

    def test_1bpp_formats(self):
        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_Mono",
            native = C(0, 0),
            memory_le = [
                C(0, 0) + Cn(1, 0, 0) + Cn(2, 0, 0) + Cn(3, 0, 0) +
                Cn(4, 0, 0) + Cn(5, 0, 0) + Cn(6, 0, 0) + Cn(7, 0, 0)],
            memory_be = [
                C(0, 0) + Cn(1, 0, 0) + Cn(2, 0, 0) + Cn(3, 0, 0) +
                Cn(4, 0, 0) + Cn(5, 0, 0) + Cn(6, 0, 0) + Cn(7, 0, 0)])

        self.assertFormatMatchesUnorm(
            format_str = "QImage::Format_MonoLSB",
            native = C(0, 0),
            memory_le = [
                Cn(7, 0, 0) + Cn(6, 0, 0) + Cn(5, 0, 0) + Cn(4, 0, 0) +
                Cn(3, 0, 0) + Cn(2, 0, 0) + Cn(1, 0, 0) + C(0, 0)],
            memory_be = [
                Cn(7, 0, 0) + Cn(6, 0, 0) + Cn(5, 0, 0) + Cn(4, 0, 0) +
                Cn(3, 0, 0) + Cn(2, 0, 0) + Cn(1, 0, 0) + C(0, 0)])

    def test_unknown_formats(self):
        self.assertFormatIsUnknown("QImage::Format_RGB565")

    def test_find_compatible(self):
        pass
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "qt",
            everywhere = ["QImage::Format_RGB16"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "qt",
            everywhere = [],
            little_endian = [
                "QImage::Format_ARGB32",
                "QImage::Format_ARGB32_Premultiplied"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "qt",
            everywhere = [],
            little_endian = [
                "QImage::Format_RGB32",
                "QImage::Format_ARGB32",
                "QImage::Format_ARGB32_Premultiplied"],
            big_endian = [],
            treat_x_as_a = True)

    def test_documentation(self):
        self.assertHasDocumentationFor("qt")
