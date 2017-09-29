# DirectFB pixel formats

DirectFB formats are packed formats which mostly follow the scheme (but see the
sections below about special cases):

    DSPF_{components}{component-bits}

These formats specify a pixel represented by a native type of the least size
(8, 16, 24 or 32 bits) that can fit the sum of `component-bits`. The
leftmost component occupies the most significant bits of the type and the
rightmost component the least significant bits.

The leftmost value in `component-bits` specifies the size of the leftmost
component in `components`, and the rightmost value in `component-bits` the size
of the rightmost component in `components`. Any unspecified bits occupy the
most significant bits of the native type, followed by the specified component
bits.

If the `component-bits` part is missing it is assumed to be `8888`.

The memory layout of packed formats depends on system endianness.

**Example: `DSPF_ARGB`**

The pixel is represented by a 32-bit value, with A in bits 24-31, R in bits
16-23, G in bits 8-15 and B in bits 0-7:

    M                                                              L
    A₇A₆A₅A₄A₃A₂A₁A₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, A
(B at the lowest address, A at the highest).

On big-endian systems the pixel is stored in memory as the bytes A, R, G, B (A
at the lowest address, B at the highest).

**Example: `DSPF_RGB555`**

The pixel is represented by a 16-bit value, with bit 15 unused, R in bits
10-14, G in bits 5-9 and B in bits 0-4:

    M                              L
    X₀R₄R₃R₂R₁R₀G₄G₃G₂G₁G₀B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    G₂G₁G₀B₄B₃B₂B₁B₀ X₀R₄R₃R₂R₁R₀G₄G₃

On big-endian systems the pixel is stored in memory as:

    0                1
    M              L M              L
    X₀R₄R₃R₂R₁R₀G₄G₃ G₂G₁G₀B₄B₃B₂B₁B₀


## Special cases: `DSPF_RGBnn` formats

Some DirectFB formats follow the scheme:

    DSPF_RGB{16,18,24,32}

The numerical suffix describes either the total number of bits or the number of
used bits in a pixel. The exact meaning of these is not consistent and is
described in the examples below.

**Example: `DSPF_RGB32`**

A 32-bit native value with bits 24-31 unused, R in bits 16-23, G in bits 8-15
and B in bits 0-7. If following the scheme from the previous section, it could
have been defined more informatively as XRGB8888.

**Example: `DSPF_RGB24`**

A 24-bit native value with R in bits 16-31, G in bits 8-15 and B in bits 0-7.
and B in bits 0-7. If following the scheme from the previous section, it could have
been defined more informatively as RGB888.

**Example: `DSPF_RGB18`**

A 24-bit native value with bits 18-24 unsued, R in bits 12-17, G in bits 6-11
and B in bits 0-5. If following the scheme from the previous section, it could
have been defined more informatively as XRGB6666.

**Example: `DSPF_RGB16`**

A 16-bit native value with R in bits 11-15, G in bits 5-10 and B in bits 0-4.
and B in bits 0-5. If following the scheme from the previous section, it could
have been defined more informatively as RGB565.

## Special cases: 4bpp and 1bpp pixel formats

DirectFB supports pixel formats that describe pixels with a size of less than 8
bits. For such pixel formats we must know how to store multiple pixels in a
byte.

If the format doesn't have an `_LSB` suffix, then the bits of a pixel in a
pixel series are stored in the most significant available bits of the current
byte. When the byte fills up, storage is moved to the next byte.

If the format has an `_LSB` suffix (only available for 1bpp formats) the bits
of a pixel in a pixel series are stored in the least significant available bits
of the current byte. When the byte fills up, storage is moved to the next byte.

To better illustrate the storage scheme, the examples below show how a series
of pixels is stored in memory.

**Example: `DSPF_A4`**

Each pixel is represented as a 4-bit value:

    M      L
    A₃A₂A₁A₀

On both big-endian and little-endiant systems the 4 pixels ABCD are stored as:

    0                1
    M              L M              L
    A₃A₂A₁A₀B₃B₂B₁B₀ C₃C₂C₁C₀D₃D₂D₁D₀

**Example: `DSPF_A1`**

Each pixel is represented as a 1-bit value:

    A₀

On both big-endian and little-endian systems the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    A₀B₀C₀D₀E₀F₀G₀H₀ I₀J₀K₀L₀M₀N₀O₀P₀

**Example: `DSPF_A1_LSB`**

Each pixel is represented as a 1-bit value:

    A₀

On both big-endian and little-endian systems the 16 pixels ABC...NOP are stored as:

    0                1
    M              L M              L
    H₀G₀F₀E₀D₀C₀B₀A₀ P₀O₀N₀M₀L₀K₀J₀I₀
