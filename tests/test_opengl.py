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

class OpenGLTest(TestCase):
    def test_non_packed_formats(self):
        self.assertFormatMatches(
            format_str = "GL_RGBA+GL_UNSIGNED_BYTE",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0), A(7, 0)])

    def test_non_packed_formats_with_multibyte_components(self):
        self.assertFormatMatches(
            format_str = "GL_RGB+GL_UNSIGNED_SHORT",
            native = None,
            memory_le = [R(7, 0), R(15, 8), G(7, 0), G(15, 8), B(7, 0), B(15, 8)],
            memory_be = [R(15, 8), R(7, 0), G(15, 8), G(7, 0), B(15, 8), B(7, 0)])

    def test_packed_formats(self):
        self.assertFormatMatches(
            format_str = "GL_BGRA+GL_UNSIGNED_INT_10_10_10_2",
            native = B(9, 0) + G(9, 0) + R(9, 0) + A(1, 0),
            memory_le = [
                R(5, 0) + A(1, 0), 
                G(3, 0) + R(9, 6),
                B(1, 0) + G(9, 4),
                B(9, 2)],
            memory_be = [
                B(9, 2),
                B(1, 0) + G(9, 4),
                G(3, 0) + R(9, 6),
                R(5, 0) + A(1, 0)])

        self.assertFormatMatches(
            format_str = "GL_RGBA+GL_UNSIGNED_INT_2_10_10_10_REV",
            native = A(1,0) + B(9,0) + G(9,0) + R(9,0),
            memory_le = [
                R(7, 0),
                G(5, 0) + R(9, 8),
                B(3, 0) + G(9, 6),
                A(1, 0) + B(9, 4)],
            memory_be = [
                A(1, 0) + B(9, 4),
                B(3, 0) + G(9, 6),
                G(5, 0) + R(9, 8),
                R(7, 0)])

    def test_single_component_formats(self):
        self.assertFormatMatches(
            format_str = "GL_RED+GL_UNSIGNED_BYTE",
            native = None,
            memory_le = [R(7, 0)],
            memory_be = [R(7, 0)])

        self.assertFormatMatches(
            format_str = "GL_GREEN+GL_UNSIGNED_BYTE",
            native = None,
            memory_le = [G(7, 0)],
            memory_be = [G(7, 0)])

        self.assertFormatMatches(
            format_str = "GL_BLUE+GL_UNSIGNED_BYTE",
            native = None,
            memory_le = [B(7, 0)],
            memory_be = [B(7, 0)])

    def test_integer_formats(self):
        self.assertFormatMatches(
            format_str = "GL_RG_INTEGER+GL_UNSIGNED_BYTE",
            native = None,
            memory_le = [R(7, 0), G(7, 0)],
            memory_be = [R(7, 0), G(7, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "opengl",
            everywhere = [
                "GL_RGB+GL_UNSIGNED_SHORT_5_6_5",
                "GL_RGB_INTEGER+GL_UNSIGNED_SHORT_5_6_5"],
            little_endian = [],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "opengl",
            everywhere = [
                "GL_BGRA+GL_UNSIGNED_BYTE",
                "GL_BGRA+GL_BYTE",
                "GL_BGRA_INTEGER+GL_UNSIGNED_BYTE",
                "GL_BGRA_INTEGER+GL_BYTE"],
            little_endian = [
                "GL_BGRA+GL_UNSIGNED_INT_8_8_8_8_REV",
                "GL_BGRA_INTEGER+GL_UNSIGNED_INT_8_8_8_8_REV"],
            big_endian = [
                "GL_BGRA+GL_UNSIGNED_INT_8_8_8_8",
                "GL_BGRA_INTEGER+GL_UNSIGNED_INT_8_8_8_8"])

        self.assertFindCompatibleMatches(
            format_str = "PIXMAN_x8r8g8b8",
            family_str = "opengl",
            everywhere = [
                "GL_BGRA+GL_UNSIGNED_INT_8_8_8_8_REV",
                "GL_BGRA_INTEGER+GL_UNSIGNED_INT_8_8_8_8_REV"],
            little_endian = [
                "GL_BGRA+GL_UNSIGNED_BYTE",
                "GL_BGRA+GL_BYTE",
                "GL_BGRA_INTEGER+GL_UNSIGNED_BYTE",
                "GL_BGRA_INTEGER+GL_BYTE"],
            big_endian = [],
            treat_x_as_a = True);

    def test_documentation(self):
        self.assertHasDocumentationFor("opengl")
