import unittest
import pfg

class TestCase(unittest.TestCase):
    def assertFormatMatches(self, format_str, native, memory_le, memory_be):
        fd = pfg.describe(format_str)
        self.assertEqual(native, fd.native)
        self.assertEqual(memory_le, fd.memory_le)
        self.assertEqual(memory_be, fd.memory_be)

    def assertHasDocumentationFor(self, family):
        documentation = pfg.document(family)
        self.assertIsNotNone(documentation)
        self.assertNotEqual("", documentation)
