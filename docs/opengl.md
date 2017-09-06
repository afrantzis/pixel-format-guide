# OpenGL pixel formats

OpenGL uses two separate definitions to fully specify a pixel format on the CPU
side, the `format` and the `type`.

## Format

The `format` specifies the logical order of components in the pixel format. It
follows the scheme:

    GL_{components-list}

**Example: `GL_RGBA`**

The pixel format consists of four components in the logical order R, G, B, A.

**Example: `GL_BGRA`**

The pixel format consists of four components in the logical order B, G, R, A.

**Example: `GL_RED`**

The pixel format consists of a single component R.

## Type

The `type` specifies the size and memory representation of the components
specified in `format`. It has two forms, one for non-packed and one for packed
representations.

### Non-packed

The non-packed representation of `type` follows the scheme:

    GL_{data-type}

The `data-type` specifies the data type of each component.  The components
are ordered in memory in the order specified by `format`. How each
component is stored in memory depends on system endianness.

**Example: `GL_UNSIGNED_BYTE`**

Each component is stored as a byte.

**Example: `GL_UNSIGNED_INT`**

Each component is stored as 32-bit native integer, and is therefore
affected by system endianness.

### Packed

The packed representation of `type` follows the scheme:

    GL_{data-type}_{component-bits}(_REV)

The `data-type` specifies the data type used to hold the pixel data as a
whole. The `component-bits` specify the number of bits each component
occupies in the data type. The leftmost number corresponds to the size of
the component which will occupy the most significant bits of the data type.
The leftmost number corresponds to the size of the component which will
occupy the least significant bits of the data type.

The way in which components will be ordered in the data type bit positions
is controlled by the existence or absence of the `REV` suffix.

If the `type` doesn't have the `REV` suffix, then the first component
occupies the most significant bits, and the last component occupies the
least significant bits. Visually, the format `GL_XYZW` will be mapped to
the data type as `0xXYZW`.

If the `type` has the `REV` suffix, then the first component occupies the
least significant bits, and the last component occupies the most
significant bits. Visually, the format `GL_XYZW` will be mapped to the data
type as `0xWZYX` (hence the `REV` designation).

The memory layout of a packed pixel format depends on system endianness.

**Example: `GL_UNSIGNED_SHORT_5_6_5`**

The pixel is represented by a 16-bit value, with the first component
in bits 11-15, the second component in bits 5-10 and the third component
in bits 0-5.

**Example: `GL_UNSIGNED_SHORT_5_6_5_REV`**

The pixel is represented by a 16-bit value, with the third component
in bits 11-15, the second component in bits 5-10 and the first component
in bits 0-5.

## Combining format and type

By combining a `format` and a `type` we get a full specification of the pixel
format. For packed `type`s the number of components in `format` and `type` must
match.

**Example: `GL_RGBA` with `GL_UNSIGNED_BYTE`**

This combination specifies a pixel format laid out in memory as the bytes
R, G, B, A (R at the lowest address, A at the highest)

**Example: `GL_RGB` with `GL_UNSIGNED_SHORT`**

The memory layout of this combination depends on system endianness. On
little-endian systems it is stored as:

    R₀, R₁, G₀, G₁, B₀, B₁

On big-endian systems it is stored as:

    R₁, R₀, G₁, G₀, B₁, B₀

(R₀, R₁ are the first and second bytes of the R component, respectively)

**Example: `GL_BGRA` with `GL_UNSIGNED_INT_10_10_10_2`**

This combination represents the 32-bit value:

    M                              L
    BBBBBBBBBBGGGGGGGGGGRRRRRRRRRRAA

The memory layout of this combination depends on system endianness. On
little-endian systems it is stored as:

    0        1        2        3
    M      L M      L M      L M      L
    RRRRRRAA GGGGRRRR BBGGGGGG BBBBBBBB

On big-endian systems it is stored as:

    0        1        2        3
    M      L M      L M      L M      L
    BBBBBBBB BBGGGGGG GGGGRRRR RRRRRRAA

**Example: `GL_RGBA` with `GL_UNSIGNED_INT_2_10_10_10_REV`**

This combination represents the 32-bit value:

    M                              L
    AABBBBBBBBBBGGGGGGGGGGRRRRRRRRRR

The memory layout of this combination depends on system endianness. On
little-endian systems it is stored as:

    0        1        2        3
    M      L M      L M      L M      L
    RRRRRRRR GGGGGGRR BBBBGGGG AABBBBBB

On big-endian systems it is stored as:

    0        1        2        3
    M      L M      L M      L M      L
    AABBBBBB BBBBGGGG GGGGGGRR RRRRRRRR

**Example: `GL_RGB` with `GL_UNSIGNED_INT_8_8_8_8`**

This combination is invalid since `GL_RGB` is a 3-component `format` and
`GL_UNSIGNED_INT_8_8_8_8` is a 4-component packed `type`.
