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
