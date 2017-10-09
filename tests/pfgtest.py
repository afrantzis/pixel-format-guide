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

import unittest
import pfg
from pfg import util

class TestCase(unittest.TestCase):
    def assertFormatMatches(self, format_str, native, memory_le, memory_be):
        fd = pfg.describe(format_str)
        self.assertEqual(native, fd.native)
        self.assertEqual(memory_le, fd.memory_le)
        self.assertEqual(memory_be, fd.memory_be)

    def assertFindCompatibleMatches(self, format_str, family_str,
                                    everywhere, little_endian, big_endian,
                                    treat_x_as_a=False):
        compatibility = pfg.find_compatible(format_str, family_str, treat_x_as_a)
        # assertCountEqual checks for the existence of items regardless
        # of order (and has a misleading name...)
        self.assertCountEqual(everywhere, compatibility.everywhere)
        self.assertCountEqual(little_endian, compatibility.little_endian)
        self.assertCountEqual(big_endian, compatibility.big_endian)

    def assertHasDocumentationFor(self, family):
        documentation = pfg.document(family)
        self.assertEqual(util.read_documentation(family + ".md"), documentation)

def R(m,l): return util.component_bits("R", m, l)
def G(m,l): return util.component_bits("G", m, l)
def B(m,l): return util.component_bits("B", m, l)
def A(m,l): return util.component_bits("A", m, l)
def X(m,l): return util.component_bits("X", m, l)
def Y(m,l): return util.component_bits("Y", m, l)
def U(m,l): return util.component_bits("U", m, l)
def V(m,l): return util.component_bits("V", m, l)
def C(m,l): return util.component_bits("C", m, l)

def Rn(n,m,l): return util.component_bits("(R+%d)" % n, m, l)
def Gn(n,m,l): return util.component_bits("(G+%d)" % n, m, l)
def Bn(n,m,l): return util.component_bits("(B+%d)" % n, m, l)
def An(n,m,l): return util.component_bits("(A+%d)" % n, m, l)
def Cn(n,m,l): return util.component_bits("(C+%d)" % n, m, l)
