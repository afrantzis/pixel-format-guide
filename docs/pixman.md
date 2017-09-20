# Pixman pixel formats

All Pixman formats are packed formats (but see the [special
cases](#special-cases-4bpp-and-1bpp-pixel-formats)).  The format definitions
follow the scheme:

    PIXMAN_{component-format}

The `component-format` part specifies the sizes and order of the components in
a native type, with the leftmost component stored in the most significant bits,
and the rightmost component in the least significant bits. Each component is
immediately followed by its size in bits (e.g. `r8`).

The memory layout of packed formats depends on system endianness.

**Example: `PIXMAN_a8r8g8b8`**

The pixel is represented by a 32-bit value, with A in bits 24-31, R in bits
16-23, G in bits 8-15 and B in bits 0-7:

    M                                                              L
    A₇A₆A₅A₄A₃A₂A₁A₀R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R, A
(B at the lowest address, A at the highest).

On big-endian systems the pixel is stored in memory as the bytes A, R, G, B (A
at the lowest address, B at the highest).

**Example: `PIXMAN_r8g8b8`**

The pixel is represented by a 24-bit value, R in bits 16-23, G in bits 8-15 and
B in bits 0-7:

    M                                              L
    R₇R₆R₅R₄R₃R₂R₁R₀G₇G₆G₅G₄G₃G₂G₁G₀B₇B₆B₅B₄B₃B₂B₁B₀

On little-endian systems the pixel is stored in memory as the bytes B, G, R
(B at the lowest address, R at the highest).

On big-endian systems the pixel is stored in memory as the bytes R, G, B (R at
the lowest address, B at the highest).

**Example: `PIXMAN_r5g6b5`**

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


## Special cases: 4bpp and 1bpp pixel formats

Pixman supports pixel formats that describe pixels with a size of less than 8
bits. For such pixel formats we must know how to store multiple pixels in a
byte. For pixman, the answer depends on system endianness.

On little-endian systems the bits of a pixel in a pixel series are stored in
the least significant available bits of the current byte. When the byte fills
up, storage is moved to the next byte.

On big-endian systems the bits of a pixel in a pixel series are stored in the
most significant available bits of the current byte. When the byte fills up,
storage is moved to the next byte.

To better illustrate the storage scheme, the examples below show how a series
of pixels is stored in memory.

**Example: `PIXMAN_a4`**

Each pixel is represented as a 4-bit value:

    M      L
    A₃A₂A₁A₀

On little-endian systems the 4 pixels ABCD are stored as:

    0                1
    M              L M              L
    B₃B₂B₁B₀A₃A₂A₁A₀ D₃D₂D₁D₀C₃C₂C₁C₀


On big-endian systems the 4 pixels ABCD are stored as:

    0                1
    M              L M              L
    A₃A₂A₁A₀B₃B₂B₁B₀ C₃C₂C₁C₀D₃D₂D₁D₀

**Example: `PIXMAN_a1`**

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
