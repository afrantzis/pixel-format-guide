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
