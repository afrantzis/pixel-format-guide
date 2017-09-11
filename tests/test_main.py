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
