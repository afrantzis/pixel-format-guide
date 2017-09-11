# Welcome to the Pixel Format Guide Tool

The Pixel Format Guide Tool is a python program that describes how the
components of various pixels formats are laid out in memory.

This tool is part of the [Pixel Format Guide](https://afrantzis.github.io/pixel-format-guide).

Development of the Pixel Format Guide is sponsored by [Collabora Ltd](https://www.collabora.com).

# How to run the Pixel Format Guide Tool

Run with:

     $ python3 -m pfg describe [FORMAT]
     $ python3 -m pfg document [FAMILY]

Examples:

    $ python3 -m pfg describe GL_RGBA+GL_UNSIGNED_INT_2_10_10_10_REV
    Format:               GL_RGBA+GL_UNSIGNED_INT_2_10_10_10_REV
    Described as:         Native 32-bit type
    Native type:          M                                                              L
                          A₁A₀B₉B₈B₇B₆B₅B₄B₃B₂B₁B₀G₉G₈G₇G₆G₅G₄G₃G₂G₁G₀R₉R₈R₇R₆R₅R₄R₃R₂R₁R₀
    Memory little-endian: 0                1                2                3
                          M              L M              L M              L M              L
                          R₇R₆R₅R₄R₃R₂R₁R₀ G₅G₄G₃G₂G₁G₀R₉R₈ B₃B₂B₁B₀G₉G₈G₇G₆ A₁A₀B₉B₈B₇B₆B₅B₄
    Memory big-endian:    0                1                2                3
                          M              L M              L M              L M              L
                          A₁A₀B₉B₈B₇B₆B₅B₄ B₃B₂B₁B₀G₉G₈G₇G₆ G₅G₄G₃G₂G₁G₀R₉R₈ R₇R₆R₅R₄R₃R₂R₁R₀

    $ python3 -m pfg describe VK_FORMAT_A2R10G10B10_UNORM_PACK32
    Format:               VK_FORMAT_A2R10G10B10_UNORM_PACK32
    Described as:         Native 32-bit type
    Native type:          M                                                              L
                          A₁A₀R₉R₈R₇R₆R₅R₄R₃R₂R₁R₀G₉G₈G₇G₆G₅G₄G₃G₂G₁G₀B₉B₈B₇B₆B₅B₄B₃B₂B₁B₀
    Memory little-endian: 0                1                2                3
                          M              L M              L M              L M              L
                          B₇B₆B₅B₄B₃B₂B₁B₀ G₅G₄G₃G₂G₁G₀B₉B₈ R₃R₂R₁R₀G₉G₈G₇G₆ A₁A₀R₉R₈R₇R₆R₅R₄
    Memory big-endian:    0                1                2                3
                          M              L M              L M              L M              L
                          A₁A₀R₉R₈R₇R₆R₅R₄ R₃R₂R₁R₀G₉G₈G₇G₆ G₅G₄G₃G₂G₁G₀B₉B₈ B₇B₆B₅B₄B₃B₂B₁B₀

    $ python3 -m pfg describe WL_DRM_FORMAT_ARGB8888
    Format:               WL_DRM_FORMAT_ARGB8888
    Described as:         Bytes in memory
    Memory little-endian: 0                1                2                3
                          M              L M              L M              L M              L
                          B₇B₆B₅B₄B₃B₂B₁B₀ G₇G₆G₅G₄G₃G₂G₁G₀ R₇R₆R₅R₄R₃R₂R₁R₀ A₇A₆A₅A₄A₃A₂A₁A₀
    Memory big-endian:    0                1                2                3
                          M              L M              L M              L M              L
                          B₇B₆B₅B₄B₃B₂B₁B₀ G₇G₆G₅G₄G₃G₂G₁G₀ R₇R₆R₅R₄R₃R₂R₁R₀ A₇A₆A₅A₄A₃A₂A₁A₀

    $ python3 -m pfg document vulkan
    # Vulkan pixel formats
    ...

    $ python3 -m pfg document wayland_drm
    # Wayland-drm pixel formats
    ...

# Contributing to the Pixel Format Guide Tool

To add support for a new pixel format family (let's call it `family`), do the
following:

* Add some tests for typical pixel formats definitions in the family
  in `tests/test_family.py`.  Use one of the existing test files as a
  template.

* Implement the `describe` method in a new `pfg/family.py` file. Use one of the
  existing files as a template.

* Implement the `document` method in the `pfg/family.py` file, by creating a
  `docs/family.md` and returning its contents (use the
  `util.read_documentation` helper).

* Import the `family` module and add it to the list of `families` in
  `pfg/commands.py`.

* Run `python3 -m unittest discover` and ensure all tests pass.

* Add a link to the new family document file in `docs/index.md`.
