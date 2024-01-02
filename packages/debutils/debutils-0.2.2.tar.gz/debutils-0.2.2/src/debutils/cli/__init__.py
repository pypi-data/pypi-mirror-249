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

from debutils.__about__ import __version__, __license__
from debutils.cli.go import go
from debutils.cli.itpwriter import itpwriter
from debutils.cli.search_db import search_db
from debutils.cli.wnpp_check import wnpp_check


def print_license(ctx: click.Context, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__license__)
    ctx.exit()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="debutils")
@click.option(
    "--license",
    is_flag=True,
    callback=print_license,
    expose_value=False,
    is_eager=True,
    help="Show copyright and license information and exit."
)
def main():
    """
    Utilities to help Debian package maintainers.
    """


main.add_command(itpwriter)
main.add_command(search_db)
main.add_command(wnpp_check)
main.add_command(go)
