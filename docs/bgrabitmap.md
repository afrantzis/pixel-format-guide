# BGRABitmap pixel formats

BGRABitmap offers a single type for pixels (`TBGRAPixel`), the format of which
is decided at compile-time. The format used depends on system details and
various compile-time definitions, which lead to the definition of the
`BGRABITMAP_BGRAPIXEL` or `BGRABITMAP_RGBAPIXEL` compile-time definitions.

If `BGRABITMAP_BGRAPIXEL` is defined or there is no format definition at all,
then the format used is an array format which is always stored in memory as the
bytes B, G, R, A (with B at the lowest address, A at the highest).

If `BGRABITMAP_RGBAPIXEL` is defined, then the format used is an array format
which is always stored in memory as the bytes R, G, B, A (with R at the lowest
address, A at the highest).
