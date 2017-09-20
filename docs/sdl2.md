# SDL2 pixel formats

The SDL2 pixel formats fall into 3 different categories: packed formats, array
formats and index formats (not described in this guide).

## Packed formats

Packed formats follow the scheme:

    SDL_PIXELFORMAT_{components}{component-bits}

They specify a pixel represented by a native type of size
`sum(component-bits)`, with the leftmost value in `component-bits` denoting the
size of the leftmost component in `components`, and the rightmost value in
`component-bits` the size of the rightmost component in `components`.

The leftmost component occupies the most significant bits of the type and the
rightmost component the least significant bits.

The memory layout of a packed pixel format depends on system endianness.

**Example: `SDL_PIXELFORMAT_RGB565`**

The pixel is represented by a 16-bit value, with R in bits 11-15, G in bits
5-10 and B in bits 0-4.

On little-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    G₂G₁G₀B₄B₃B₂B₁B₀ R₄R₃R₂R₁R₀G₅G₄G₃

On big-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    R₄R₃R₂R₁R₀G₅G₄G₃ G₂G₁G₀B₄B₃B₂B₁B₀

**Example: `SDL_PIXELFORMAT_ARGB8888`**

The pixel is represented by a 32-bit value, with A in bits (24-31), R in bits
16-23, G in bits 8-15 and B in bits 0-7.

On little-endian systems the pixel is stored in memory as the bytes B, G, R, A
(B at the lowest address, A at the highest).

On big-endian systems the pixel is stored in memory as the bytes A, R, G, B (A
at the lowest address, B at the highest).

## Array formats

Array formats follow the scheme:

    SDL_PIXELFORMAT_{components}{24,32}

They specify a pixel stored in memory as an array of either 3 (suffix `24`) or
4 (suffix `32`) consecutive bytes with each component occupying a single byte.
The leftmost component is stored at the lowest memory address, and the
rightmost component is stored at the highest memory address.

**Example: `SDL_PIXELFORMAT_RGB24`**

Stored in memory as the bytes R, G, B (R at the lowest address, B at the
highest address).

**Example: `SDL_PIXELFORMAT_ABGR32`**

Stored in memory as the bytes A, B, G, R (A at the lowest address, R at the
highest address).
