# Qt pixel formats

Qt pixel formats are mostly packed formats with a few exceptions listed in the
"Special Case" sections. The format definitions follow the scheme:

    QImage::Format_{components}{sizes}(_Premultiplied)

The `components` part specifies the order of the components in a native type,
with the leftmost component stored in the most significant bits, and the
rightmost component in the least significant bits.

Unfortunately, the format definitions are not consistent in the way they
represent component sizes.  The `sizes` part either specifies the total size of
the pixel in bits, or the total number of bits used by the defined components
(i.e., not including unused bits), or the size of each component in bits. Use
the [pfg tool](https://github.com/afrantzis/pixel-format-guide) or consult the
Qt documentation to find the exact meaning of `sizes` for each format
definition.

The `_Premultiplied` suffix indicates that this is a premultiplied alpha
format.

Since Qt pixel formats are packed format, the memory layout of these formats
depends on system endianness.

**Example: `QImage::Format_ARGB32`**

The pixel is represented by a 32-bit value, with A in bits 24-31, R in bits
16-23, G in bits 8-15 and B in bits 0-7:

    M                                                              L
    A₇A₆A₅A₄A₃A₂A₁A₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, A
(B at the lowest address, A at the highest).

On big-endian systems the pixel is stored in memory as the bytes A, R, G, B (A
at the lowest address, B at the highest).

**Example: `QImage::Format_RGB32`**

The pixel is represented by a 32-bit value, with R in bits 16-23, G in bits 8-15,
B in bits 0-7, with the bits 24-31 being unused:

    M                                                              L
    X₇X₆X₅X₄X₃X₂X₁X₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, X
(B at the lowest address, X at the highest).

On big-endian systems the pixel is stored in memory as the bytes X, R, G, B, (X at
the lowest address, B at the highest).

**Example: `QImage::Format_ARGB8555_Premultiplied`**

The pixel is represented by a 24-bit value, with the most significant bit
unused, A in bits 15-22, R in bits 10-14, G in bits 5-9 and B in bits 0-4:

    M                                              L
    X₀A₇A₆A₅A₄A₃A₂A₁A₀R₄R₃R₂R₁R₀G₄G₃G₂G₁G₀B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as:

    0                1                2
    M              L M              L M              L
    G₂G₁G₀B₄B₃B₂B₁B₀ A₀R₄R₃R₂R₁R₀G₄G₃ X₀A₇A₆A₅A₄A₃A₂A₁

On big-endian systems the pixel is stored in memory as:

    0                1                2
    M              L M              L M              L
    X₀A₇A₆A₅A₄A₃A₂A₁ A₀R₄R₃R₂R₁R₀G₄G₃ G₂G₁G₀B₄B₃B₂B₁B₀

## Special case: Byte array formats

Qt 5.2 introduced three byte array formats:

    QImage::Format_RGBX8888
    QImage::Format_RGBA8888
    QImage::Format_RGBA8888_Premultiplied

These formats represent pixels that are are always stored in memory as the
bytes R, G, B, A/X, with R at the lowest address and A/X at the highest
address.

## Special case: 1bpp pixel format

Qt supports the `QImage::Format_Mono` and `QImage::Format_MonoLSB` that
describe pixels with a size of a single bit. The way multiple pixels of this
format are stored in a byte depends on the format.

When using the `QImage::Format_Mono` format, the bit of a pixel in a pixel
series is stored in the most significant available bit of the current byte.
When the byte fills up, storage is moved to the next byte.

When using the `QImage::Format_MonoLSB` format, the bit of a pixel in a pixel
series is stored in the least significant available bit of the current byte.
When the byte fills up, storage is moved to the next byte.

To better illustrate the storage scheme, the examples below show how a series
of pixels is stored in memory.

**Example: `QImage::Format_Mono`**

Each pixel is represented as a 1-bit value:

    A₀

In memory the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    A₀B₀C₀D₀E₀F₀G₀H₀ I₀J₀K₀L₀M₀N₀O₀P₀


**Example: `QImage::Format_MonoLSB`**

Each pixel is represented as a 1-bit value:

    A₀

In memory the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    H₀G₀F₀E₀D₀C₀B₀A₀ P₀O₀N₀M₀L₀K₀J₀I₀
