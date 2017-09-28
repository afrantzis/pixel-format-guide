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

from .pfgtest import TestCase, R, G, B, A, Y, U, V

class WaylandDRMTest(TestCase):
    def test_rgba_formats(self):
        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_RGBA8888",
            native = None,
            memory_le = [A(7, 0), B(7, 0), G(7, 0), R(7, 0)],
            memory_be = [A(7, 0), B(7, 0), G(7, 0), R(7, 0)])

        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_ARGB2101010",
            native = None,
            memory_le = [B(7, 0), G(5, 0) + B(9, 8), R(3, 0) + G(9, 6), A(1, 0) + R(9, 4)],
            memory_be = [B(7, 0), G(5, 0) + B(9, 8), R(3, 0) + G(9, 6), A(1, 0) + R(9, 4)])

    def test_yuv_packed_formats(self):
        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_YUYV",
            native = None,
            memory_le = [Y(7, 0), U(7, 0), Y(7, 0), V(7, 0)],
            memory_be = [Y(7, 0), U(7, 0), Y(7, 0), V(7, 0)])

    def test_find_compatible(self):
        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            family_str = "wayland_drm",
            everywhere = [],
            little_endian = ["WL_DRM_FORMAT_RGB565"],
            big_endian = [])

        self.assertFindCompatibleMatches(
            format_str = "VK_FORMAT_B8G8R8A8_UNORM",
            family_str = "wayland_drm",
            everywhere = ["WL_DRM_FORMAT_ARGB8888"],
            little_endian = [],
            big_endian = [])

    def test_documentation(self):
        self.assertHasDocumentationFor("wayland_drm")
