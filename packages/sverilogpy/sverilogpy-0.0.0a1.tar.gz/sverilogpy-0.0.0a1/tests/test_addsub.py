#####################################################################################
# A python System Verilog Parser and AST
# Copyright (C) 2024  RISCY-Lib Contributors
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <https://www.gnu.org/licenses/>.
#####################################################################################

import sverilogpy_bind


def test_sub():
  assert (sverilogpy_bind.sub(1, 1) == 0)
  assert (sverilogpy_bind.sub(2, 1) == 1)
  assert (sverilogpy_bind.sub(2, 2) == 0)
  assert (sverilogpy_bind.sub(2, 3) == -1)


def test_add():
  assert (sverilogpy_bind.add(1, 1) == 2)
  assert (sverilogpy_bind.add(2, 1) == 3)
  assert (sverilogpy_bind.add(2, 2) == 4)
  assert (sverilogpy_bind.add(2, 3) == 5)
