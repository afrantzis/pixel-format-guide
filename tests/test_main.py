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
        self.orig_stderr, sys.stderr = sys.stderr, StringIO()

    def tearDown(self):
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr

    def get_stdout_stderr(self):
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        return sys.stdout.read(), sys.stderr.read()

    def get_stdout_without_error(self):
        output, error = self.get_stdout_stderr()
        self.assertEqual("", error)
        return output

    def get_stderr_without_output(self):
        output, error = self.get_stdout_stderr()
        self.assertEqual("", output)
        return error

    def test_describes_format_with_native_description(self):
        pfg.main(["pfg.py", "describe", "VK_FORMAT_R5G6B5_UNORM_PACK16"])
        description = pfg.describe("VK_FORMAT_R5G6B5_UNORM_PACK16")

        output = self.get_stdout_without_error()

        self.assertIn(native_to_str(description.native), output)
        self.assertIn(memory_to_str(description.memory_le), output)
        self.assertIn(memory_to_str(description.memory_be), output)
        self.assertIn("Native 16-bit type", output)

    def test_describes_format_without_native_description(self):
        pfg.main(["pfg.py", "describe", "VK_FORMAT_R8G8A8_UNORM"])
        description = pfg.describe("VK_FORMAT_R8G8A8_UNORM")

        output = self.get_stdout_without_error()

        self.assertIn(" " + description.data_type, output)
        self.assertIn(memory_to_str(description.memory_le), output)
        self.assertIn(memory_to_str(description.memory_be), output)
        self.assertIn("Bytes in memory", output)

    def test_describes_format_without_bit_indices(self):
        pfg.main(["pfg.py", "describe", "--hide-bit-indices", "VK_FORMAT_R5G6B5_UNORM_PACK16"])
        description = pfg.describe("VK_FORMAT_R5G6B5_UNORM_PACK16")

        output = self.get_stdout_without_error()

        self.assertIn(" " + description.data_type, output)
        self.assertIn(remove_subscripts(native_to_str(description.native)), output)
        self.assertIn(remove_subscripts(memory_to_str(description.memory_le)), output)
        self.assertIn(remove_subscripts(memory_to_str(description.memory_be)), output)
        self.assertIn("Native 16-bit type", output)

    def test_reports_unknown_format(self):
        pfg.main(["pfg", "describe", "unknown_format"])

        error = self.get_stderr_without_output()

        self.assertIn("Unknown", error)
        self.assertIn("unknown_format", error)

    def test_displays_family_documentation(self):
        pfg.main(["pfg", "document", "vulkan"])
        doc = pfg.document("vulkan")

        output = self.get_stdout_without_error()

        self.assertEqual(doc + "\n", output)

    def test_reports_no_family_documentation(self):
        pfg.main(["pfg", "document", "unknown_family"])

        error = self.get_stderr_without_output()

        self.assertIn("Unknown", error)
        self.assertIn("unknown_family", error)

    def test_finds_compatible_formats(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8_UNORM", "opengl"])
        compatibility = pfg.find_compatible("VK_FORMAT_B8G8R8A8_UNORM", "opengl")

        output = self.get_stdout_without_error()

        for f in compatibility.everywhere:
            self.assertIn(f, output)
        for f in compatibility.little_endian:
            self.assertIn(f, output)
        for f in compatibility.big_endian:
            self.assertIn(f, output)

    def test_finds_compatible_formats_treating_x_as_a(self):
        pfg.main([
            "pfg", "find-compatible", "--treat-x-as-a",
            "VK_FORMAT_B8G8R8A8_UNORM", "wayland_drm"])
        compatibility = pfg.find_compatible(
            "VK_FORMAT_B8G8R8A8_UNORM", "wayland_drm", treat_x_as_a=True)

        output = self.get_stdout_without_error()

        for f in compatibility.everywhere:
            self.assertIn(f, output)
        for f in compatibility.little_endian:
            self.assertIn(f, output)
        for f in compatibility.big_endian:
            self.assertIn(f, output)

    def test_reports_unknown_format_for_find_compatible(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8", "opengl"])

        error = self.get_stderr_without_output()

        self.assertIn("Unknown", error)
        self.assertIn("VK_FORMAT_B8G8R8A8", error)
        self.assertIn("opengl", error)

    def test_reports_unknown_family_for_find_compatible(self):
        pfg.main(["pfg", "find-compatible", "VK_FORMAT_B8G8R8A8_UNORM", "unknown_family"])

        error = self.get_stderr_without_output()

        self.assertIn("Unknown", error)
        self.assertIn("VK_FORMAT_B8G8R8A8_UNORM", error)
        self.assertIn("unknown_family", error)

    def test_lists_families(self):
        pfg.main(["pfg", "list-families"])
        families = pfg.list_families()

        output = self.get_stdout_without_error()

        for f in families:
            self.assertIn(f, output)

    def test_lists_formats(self):
        pfg.main(["pfg", "list-formats", "cairo"])
        formats = pfg.list_formats("cairo")

        output = self.get_stdout_without_error()

        for f in formats:
            self.assertIn(f, output)

    def test_reports_unknown_family_for_list_formats(self):
        pfg.main(["pfg", "list-formats", "unknown_family"])
        formats = pfg.list_formats("unknown_family")

        error = self.get_stderr_without_output()

        self.assertIn("Unknown", error)
        self.assertIn("unknown_family", error)
