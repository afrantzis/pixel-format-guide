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

import unittest
import sys
import pfg
from io import StringIO

def native_to_str(native):
    return "".join(native)

def memory_to_str(memory):
    return " ".join(("".join(b) for b in memory))

def remove_subscripts(s):
    return "".join((c for c in s if c not in pfg.util.subscripts))

class MainTest(unittest.TestCase):
    def setUp(self):
        self.orig_stdout, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.orig_stdout

    def test_describes_format_with_native_description(self):
        pfg.main(["pfg.py", "describe", "VK_FORMAT_R5G6B5_UNORM_PACK16"])
        description = pfg.describe("VK_FORMAT_R5G6B5_UNORM_PACK16")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn(native_to_str(description.native), output)
        self.assertIn(memory_to_str(description.memory_le), output)
        self.assertIn(memory_to_str(description.memory_be), output)
        self.assertIn("Native 16-bit type", output)

    def test_describes_format_without_native_description(self):
        pfg.main(["pfg.py", "describe", "VK_FORMAT_R8G8A8_UNORM"])
        description = pfg.describe("VK_FORMAT_R8G8A8_UNORM")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn(memory_to_str(description.memory_le), output)
        self.assertIn(memory_to_str(description.memory_be), output)
        self.assertIn("Bytes in memory", output)

    def test_describes_format_without_bit_indices(self):
        pfg.main(["pfg.py", "describe", "--hide-bit-indices", "VK_FORMAT_R5G6B5_UNORM_PACK16"])
        description = pfg.describe("VK_FORMAT_R5G6B5_UNORM_PACK16")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn(remove_subscripts(native_to_str(description.native)), output)
        self.assertIn(remove_subscripts(memory_to_str(description.memory_le)), output)
        self.assertIn(remove_subscripts(memory_to_str(description.memory_be)), output)
        self.assertIn("Native 16-bit type", output)

    def test_reports_unknown_format(self):
        pfg.main(["pfg", "describe", "unknown_format"])
        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn("Unknown", output)
        self.assertIn("unknown_format", output)

    def test_displays_family_documentation(self):
        pfg.main(["pfg", "document", "vulkan"])
        doc = pfg.document("vulkan")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertEqual(doc + "\n", output)

    def test_reports_no_family_documentation(self):
        pfg.main(["pfg", "document", "unknown_family"])

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn("Unknown", output)
        self.assertIn("unknown_family", output)

    def test_finds_compatible_formats(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8_UNORM", "opengl"])
        compatibility = pfg.find_compatible("VK_FORMAT_B8G8R8A8_UNORM", "opengl")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        for f in compatibility.everywhere:
            self.assertIn(f, output)
        for f in compatibility.little_endian:
            self.assertIn(f, output)
        for f in compatibility.big_endian:
            self.assertIn(f, output)

    def test_reports_unknown_format_for_find_compatible(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8", "opengl"])

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn("Unknown", output)
        self.assertIn("VK_FORMAT_B8G8R8A8", output)
        self.assertIn("opengl", output)

    def test_reports_unknown_family_for_find_compatible(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8_UNORM", "unknown_family"])

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn("Unknown", output)
        self.assertIn("VK_FORMAT_B8G8R8A8_UNORM", output)
        self.assertIn("unknown_family", output)

    def test_lists_families(self):
        pfg.main(["pfg", "list-families"])
        families = pfg.list_families()

        sys.stdout.seek(0)
        output = sys.stdout.read()

        for f in families:
            self.assertIn(f, output)
