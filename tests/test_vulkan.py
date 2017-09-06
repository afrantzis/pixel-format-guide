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

class VulkanTest(pfgtest.TestCase):
    def test_non_packed_formats(self):
        self.assertFormatMatches(
            format_str = "VK_FORMAT_R8G8B8A8_SRGB",
            native = None,
            memory_le = ["R" * 8, "G" * 8, "B" * 8, "A" * 8],
            memory_be = ["R" * 8, "G" * 8, "B" * 8, "A" * 8]);

    # TODO: Express the internal order of multibyte components
    def test_non_packed_formats_with_multibyte_components(self):
        self.assertFormatMatches(
            format_str = "VK_FORMAT_R16G16_UNORM",
            native = None,
            memory_le = ["R" * 8, "R" * 8, "G" * 8, "G" * 8],
            memory_be = ["R" * 8, "R" * 8, "G" * 8, "G" * 8])

    def test_packed_formats(self):
        self.assertFormatMatches(
            format_str = "VK_FORMAT_R5G6B5_UNORM_PACK16",
            native = "R" * 5 + "G" * 6 + "B" * 5,
            memory_le = ["G" * 3 + "B" * 5, "R" * 5 + "G" * 3],
            memory_be = ["R" * 5 + "G" * 3, "G" * 3 + "B" * 5])

        self.assertFormatMatches(
            format_str = "VK_FORMAT_A2R10G10B10_UNORM_PACK32",
            native = "A" * 2 + "R" * 10 + "G" * 10 + "B" * 10,
            memory_le = [
                "B" * 8,
                "G" * 6 + "B" * 2,
                "R" * 4 + "G" * 4,
                "A" * 2 + "R" * 6],
            memory_be = [
                "A" * 2 + "R" * 6,
                "R" * 4 + "G" * 4,
                "G" * 6 + "B" * 2,
                "B" * 8])

    def test_documentation(self):
        self.assertHasDocumentationFor("vulkan")
