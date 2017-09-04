import unittest
import sys
import pfg
from io import StringIO

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

        self.assertIn(description.native, output)
        self.assertIn(" ".join(description.memory_le), output)
        self.assertIn(" ".join(description.memory_be), output)
        self.assertIn("Native 16-bit type", output)

    def test_describes_format_without_native_description(self):
        pfg.main(["pfg.py", "describe", "VK_FORMAT_R8G8A8_UNORM"])
        description = pfg.describe("VK_FORMAT_R8G8A8_UNORM")

        sys.stdout.seek(0)
        output = sys.stdout.read()

        self.assertIn(" ".join(description.memory_le), output)
        self.assertIn(" ".join(description.memory_be), output)
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
