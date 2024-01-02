# debutils -- Utilities to help Debian package maintainers.
# Copyright (C) 2023 Maytham Alsudany <maytha8thedev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click

from debutils.cli.go.debian_name import debian_name
from debutils.cli.go.estimate import estimate
from debutils.cli.go.make import make
from debutils.exec import need_exec


@click.group()
@need_exec(['go'])
def go():
    """
    Collection of utilities to help with packaging Go modules.
    """


go.add_command(debian_name)
go.add_command(estimate)
go.add_command(make)

