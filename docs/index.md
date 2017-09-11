# Welcome to the Pixel Format Guide

The Pixel Format Guide is a repository of descriptions of various pixel formats
and the layout of their components in memory.

Different projects and APIs use different pixel format definitions, and the
information about how to interpret them is often not easily discoverable, or
even non-existent. By centralizing the information, I hope to make life easier
for everyone that needs to deal with pixel formats.

Note that this guide is not meant to provide an exhaustive list of all pixel
formats within families, but rather high-level descriptions and guidelines
about how to interpret them. Also, note that this guide currently describes
only single-plane, non-compressed formats since these are both the most common
formats and also the ones that provide the greatest opportunity for confusion.

Accompanying this guide is the [pfg tool](https://github.com/afrantzis/pixel-format-guide)
that you can use to quickly get a description of a given pixel format.

Development of the Pixel Format Guide is sponsored by
[Collabora Ltd](https://www.collabora.com).

# Describing pixel formats

There are two main ways to describe the components of a typical pixel format:

* As bytes (or parts of bytes) in memory in a fixed order (often called array formats)

* As bit ranges in a native type (often called packed formats)

In the first case, the memory layout does not depend on system endianness. For
example, we can describe a format, let's call it `R8G8B8A8_array`, which on all
systems, regardless of endianness, is laid out in memory as the consecutive
bytes R, G, B, A, with R at the lowest memory address and A at the highest.

In the second case, the memory layout depends on system endianness. For
example, we can describe a format, let's call it `R8G8B8A8_native`, which on
all systems is expressed as the native 32-bit integer 0xRRGGBBAA. This is
stored in memory as A, B, G, R on little-endian systems, but as R, G, B, A on
big-endian systems.

Note that in both cases the way we translate between the format name and the
memory bytes or native type is just a matter of convention. We might as well
have a `R8G8B8A8_native` format that describes an 0xAABBGGRR integer. This
guide and the [pfg tool](https://github.com/afrantzis/pixel-format-guide) will
help you understand the conventions used by the various pixel format families.

# Pixel format descriptions

* [OpenGL pixel formats](opengl.md)
* [SDL2 pixel formats](sdl2.md)
* [Vulkan pixel formats](vulkan.md)
* [Wayland-drm pixel formats](wayland_drm.md)
