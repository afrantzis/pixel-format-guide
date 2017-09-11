# Copyright © 2017 Collabora Ltd.
#
# This file is part of pfg.
#
# pfg is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# pfg is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
# more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pfg. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Alexandros Frantzis <alexandros.frantzis@collabora.com>

from .pfgtest import TestCase, R, G, B, A

class SDL2Test(TestCase):
    def test_packed_formats(self):
        self.assertFormatMatches(
            format_str = "SDL_PIXELFORMAT_RGB332",
            native = R(2, 0) + G(2, 0) + B(1, 0),
            memory_le = [R(2, 0) + G(2, 0) + B(1, 0)],
            memory_be = [R(2, 0) + G(2, 0) + B(1, 0)])

        self.assertFormatMatches(
            format_str = "SDL_PIXELFORMAT_RGB565",
            native = R(4, 0) + G(5, 0) + B(4, 0),
            memory_le = [G(2, 0)+ B(4, 0), R(4, 0) + G(5, 3)],
            memory_be = [R(4, 0) + G(5, 3), G(2, 0) + B(4, 0)])

        self.assertFormatMatches(
            format_str = "SDL_PIXELFORMAT_ARGB2101010",
            native = A(1, 0) + R(9, 0) + G(9, 0) + B(9, 0),
            memory_le = [
                B(7, 0),
                G(5, 0) + B(9, 8),
                R(3, 0) + G(9, 6),
                A(1, 0) + R(9, 4)],
            memory_be = [
                A(1, 0) + R(9, 4),
                R(3, 0) + G(9, 6),
                G(5, 0) + B(9, 8),
                B(7, 0)])

    def test_array_formats(self):
        self.assertFormatMatches(
            format_str = "SDL_PIXELFORMAT_RGB24",
            native = None,
            memory_le = [R(7, 0), G(7, 0), B(7, 0)],
            memory_be = [R(7, 0), G(7, 0), B(7, 0)])

        self.assertFormatMatches(
            format_str = "SDL_PIXELFORMAT_BGRA32",
            native = None,
            memory_le = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)],
            memory_be = [B(7, 0), G(7, 0), R(7, 0), A(7, 0)])
