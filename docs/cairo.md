# Cairo pixel formats

All Cairo formats are packed formats (but see the [special
case](#special-case-1bpp-pixel-format)).  The format definitions
follow the scheme:

    CAIRO_FORMAT_{components}{total-size}(_{sizes})

The `components` part specifies the order of the components in
a native type, with the leftmost component stored in the most significant bits,
and the rightmost component in the least significant bits. The total size of
the bits of the components is specified in `total-size`.

If `sizes` is not present, then the size in bits of each component is equal to
the `total-size` divided by the number of components.

If `sizes` is present, then the size in bits of each component is specified by
the corresponding digit in `sizes`.

Formats with total sizes not matching the size of a native type (8, 16 or 32
bits) are stored in the native type of the least size that can fit them (e.g.,
a format with `total-size` of 24 is stored in a 32-bit type). Any unused bits
are always the most significant bits, followed by the components in the order
specified in `components`.

The memory layout of Cairo formats depends on system endianness.

**Example: `CAIRO_FORMAT_ARGB32`**

The pixel is represented by a 32-bit value, with A in bits 24-31, R in bits
16-23, G in bits 8-15 and B in bits 0-7:

    M                                                              L
    A₇A₆A₅A₄A₃A₂A₁A₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, A
(B at the lowest address, A at the highest).

On big-endian systems the pixel is stored in memory as the bytes A, R, G, B (A
at the lowest address, B at the highest).

**Example: `CAIRO_FORMAT_RGB24`**

The pixel is represented by a 32-bit value, with R in bits 16-23, G in bits 8-15,
B in bits 0-7, with the bits 24-31 being unused:

    M                                                              L
    X₇X₆X₅X₄X₃X₂X₁X₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, X
(B at the lowest address, X at the highest).

On big-endian systems the pixel is stored in memory as the bytes X, R, G, B, (X at
the lowest address, B at the highest).

**Example: `CAIRO_FORMAT_RGB16_565`**

The pixel is represented by a 16-bit value, with R in bits 11-15, G in bits
5-10 and B in bits 0-4:

    M                              L
    R₄R₃R₂R₁R₀G₅G₄G₃G₂G₁G₀B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    G₂G₁G₀B₄B₃B₂B₁B₀ R₄R₃R₂R₁R₀G₅G₄G₃

On big-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    R₄R₃R₂R₁R₀G₅G₄G₃ G₂G₁G₀B₄B₃B₂B₁B₀


## Special case: 1bpp pixel format

Cairo supports the `CAIRO_FORMAT_A1` pixel format that describes pixels with a
size of a single bit. The way multiple pixels of this format are stored in a byte
depends on system endianness.

On little-endian systems the bit of a pixel in a pixel series is stored in
the least significant available bit of the current byte. When the byte fills
up, storage is moved to the next byte.

On big-endian systems the bit of a pixel in a pixel series is stored in the
most significant available bit of the current byte. When the byte fills up,
storage is moved to the next byte.

To better illustrate the storage scheme, the examples below show how a series
of pixels is stored in memory.

**Example: `CAIRO_FORMAT_A1`**

Each pixel is represented as a 1-bit value:

    A₀

On little-endian systems the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    H₀G₀F₀E₀D₀C₀B₀A₀ P₀O₀N₀M₀L₀K₀J₀I₀


On big-endian systems the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    A₀B₀C₀D₀E₀F₀G₀H₀ I₀J₀K₀L₀M₀N₀O₀P₀
