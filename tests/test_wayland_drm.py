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

class WaylandDRMTest(pfgtest.TestCase):
    def test_rgba_formats(self):
        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_RGBA8888",
            native = None,
            memory_le = ["A" * 8, "B" * 8, "G" * 8, "R" * 8],
            memory_be = ["A" * 8, "B" * 8, "G" * 8, "R" * 8])

        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_ARGB2101010",
            native = None,
            memory_le = ["B" * 8, "G" * 6 + "B" * 2, "R" * 4 + "G" * 4, "A" * 2 + "R" * 6],
            memory_be = ["B" * 8, "G" * 6 + "B" * 2, "R" * 4 + "G" * 4, "A" * 2 + "R" * 6])

    def test_yuv_packed_formats(self):
        self.assertFormatMatches(
            format_str = "WL_DRM_FORMAT_YUYV",
            native = None,
            memory_le = ["Y" * 8, "U" * 8, "Y" * 8, "V" * 8],
            memory_be = ["Y" * 8, "U" * 8, "Y" * 8, "V" * 8])

    def test_documentation(self):
        self.assertHasDocumentationFor("wayland_drm")
