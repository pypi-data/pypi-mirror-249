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

from debutils.wnpp import get_itp, get_rfp, search_itps, search_rfps


@click.command()
@click.argument("package")
@click.option(
    "--fuzzy",
    "method",
    flag_value="fuzzy",
    default=True,
    show_default=True,
    help="Search for wnpp bugs that contain the given package name.",
)
@click.option(
    "--exact",
    "method",
    flag_value="exact",
    help="Find the wnpp bug that matches the given package name exactly.",
)
def wnpp_check(package, method):
    """
    Check if an ITP or RFP exists for the given package name.
    """
    match method:
        case "fuzzy":
            for itp in search_itps(package):
                click.echo(f"[#{itp[0]}] ITP: {itp[1]} -- {itp[2]}")
            for rfp in search_rfps(package):
                click.echo(f"[#{rfp[0]}] RFP: {rfp[1]} -- {rfp[2]}")
        case "exact":
            if itp := get_itp(package):
                click.echo(f"[#{itp[0]}] ITP: {itp[1]} -- {itp[2]}")
            elif rfp := get_rfp(package):
                click.echo(f"[#{rfp[0]}] RFP: {rfp[1]} -- {rfp[2]}")
