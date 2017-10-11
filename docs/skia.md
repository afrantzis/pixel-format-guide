# Skia pixel formats

The Skia pixel formats fall into 3 different categories: packed formats, array
formats and index formats (not described in this guide). All formats follow the
scheme:

    k{components}_{component-bits}_SkColorType

The `components` and `component-bits` part specify the order and sizes of the
components in the pixel.

Formats where all components are 8 bits are array formats, and the component
order as specified in `components` refers to the memory order, with the
leftmost component occupying the lowest memory address and the rightmost
component occupying the highest memory address.

Other formats are considered packed, and the component order as specified in
`components` refers to their order in a native type, with the leftmost
component occupying the most significant bits, and the rightmost occupying the
least significant bits.

Skia doesn't officially support big-endian architectures, so the memory layout
of packed formats is currently considered to always be that of the native type
**on a little-endian system**.

## Special cases

**Example: `kARGB_4444_SkColorType`**

This is a packed format, but the component order in the name is incorrect. The
format is actually 0xRGBA (not 0xARGB as the name indicates) with each
component occupying 4 bits.

**Example: `kRGBA_F16_SkColorType`**

This is an array format where each component is a 16-bit float (i.e., a
half-float) stored in memory in little-endian order. The memory layout of this
format is: R₀, R₁, G₀, G₁, B₀, B₁, A₀, A₁ with R₀ at the lowest address and A₁
at the highest address (R₀ and R₁ refer to the low and high byte of the R
component , respectively).
