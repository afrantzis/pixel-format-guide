# Vulkan pixel formats

The pixel formats in Vulkan usually follow the scheme:

    VK_FORMAT_{component-format|compression-scheme}_{numeric-format}

optionally followed by the suffix `_PACKnn` or `_BLOCK`.

The `component-format` part specifies the sizes and order of the components.
Each component is immediately followed by its size in bits (e.g. `R8`). The
`numeric-format` part describes the type of each component.

There are broadly three categories of Vulkan formats:

* Non-packed formats: `VK_FORMAT_{componenent-format}_{numeric-format}`
    
    The `component-format` specifies the order and sizes of the components in
    memory, with the leftmost component stored at the lowest address and the
    rightmost component at the highest address. When a component consists of
    multiple bytes, the order of the bytes depends on system endianness.

    **Example: `VK_FORMAT_R8G8B8A8_SRGB`**

    Always stored as R, G, B, A in memory
        (R at the lowest address, A at the highest)

    **Example: `VK_FORMAT_R16G16_UNORM`**

    Stored as R₀, R₁, G₀, G₁ in memory on little-endian systems
        (R₀ at lowest address, G₁ at highest)

    Stored as R₁, R₀, G₁, G₀ in memory on big-endian systems
        (R₁ at lowest address, G₀ at highest)

    (R₀, R₁ are the first and second bytes of the R component, respectively)

* Packed formats: `VK_FORMAT_{component-format}_{numeric-format}_PACKnn`

    The `component-format` specifies the order and sizes of the components in a
    nn-bit native type, with the leftmost component stored in the most
    significant bits, and the rightmost component in the least significant
    bits.

    The memory layout of packed formats depends on system endianness.

    **Example: `VK_FORMAT_R5G6B5_UNORM_PACK16`**

    Stored in memory in the same way a 16-bit native type would be stored on
    the system. R is in bits 11-15 of the native type, G in bits 5-10 and B in
    bits 0-4.

* Block/compressed formats

    We won't describe these in detail in this guide.
