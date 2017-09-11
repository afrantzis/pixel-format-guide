# Wayland-drm pixel formats

The wayland-drm pixel formats follow the scheme:

    WL_DRM_FORMAT_{component-format}

The `component-format` part specifies the order and sizes of the components.
All the components are listed first, optionally followed by their corresponding sizes
in bits (e.g., `RGB888`, `YUVY`).

The wayland-drm formats are a subset of the drm fourcc formats.

There are a few categories of wayland-drm formats:

* RGBA formats: `WL_DRM_FORMAT_{rgba-componenent-format}`

    The `rgba-component-format` specifies the order and sizes of the components
    in a native type **on a little-endian system**, with the leftmost component
    stored in the most significant bits, and the rightmost in the least
    significant bits.

    Although the formats are expressed in terms of a native type, the addition
    of little-endianness specification makes the format endianness-independent.

    For formats where components occupy whole bytes, an alternative, and
    probably more straightforward way to express the expected order, is that
    the `component-list` specifies the order of the components in memory with
    the leftmost component at the highest address and the rightmost at the
    lowest addres.

    Example: `WL_DRM_FORMAT_ARGB8888`

    Always stored as B, G, R, A in memory (B at lowest address, A at highest)

    Example: `VK_FORMAT_RGB565`

    Always stored in memory as:

        0                1
        M              L M              L
        G₂G₁G₀B₄B₃B₂B₁B₀ R₄R₃R₂R₁R₀G₅G₄G₃

* Packed Y'CbCr: `WL_DRM_FORMAT_{yuva-componenent-format}`

    The `yuva-component-format` specifies the order of the components in a 32-bit
    native type **on a little-endian system**, with the leftmost component stored
    in the least significant bits, and the rightmost in the most significant
    bits. In this format category each components is always 8 bits long.

    An alternative, and probably more straightforward way to interpret the
    `yuva-component-format`, is that it specifies the order of the components
    in memory with the leftmost component at the lowest address and the
    rightmost at the highest.

    Example: `WL_DRM_FORMAT_YUYV`

    Always stored as Y₀, U, Y₁, V in memory (Y₀ at lowest address, V at the highest)

* Multi-plane formats:

    We won't describe these in detail in this guide.
