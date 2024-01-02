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

from debutils.go.hosts import KNOWN_HOSTS


def debian_source_name_from_go_package(package: str, echo=False):
    parts = package.lower().split("/")
    parts[0] = short_host(parts[0], echo)
    return "golang-" + "-".join(parts)


def short_host(host: str, echo=False) -> str:
    if host in KNOWN_HOSTS:
        return KNOWN_HOSTS[host]
    short_host = ".".join(host.split(".")[:-1])
    if echo:
        click.secho(
            f"Using {short_host} as canonical hostname for {host}.", fg="yellow"
        )
        click.secho(
            "Please create an issue at https://codeberg.org/Maytha8/debutils if that is not ok.",
            fg="yellow",
        )
    return short_host
