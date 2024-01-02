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

from pathlib import Path
import re
from typing import IO

import click
from debian.changelog import Changelog
from debian.copyright import Copyright
from debian.deb822 import Deb822
from jinja2 import Environment, PackageLoader, select_autoescape


@click.command()
@click.argument("output", type=click.File("wb"), default="-")
@click.option(
    "--name",
    envvar="DEBFULLNAME",
    help="Name of package maintainer. Uses DEBFULLNAME environment variable by default.",
)
@click.option(
    "--email",
    envvar="DEBEMAIL",
    help="Email of package maintainer. Uses DEBEMAIL environment variable by default.",
)
def itpwriter(output: IO, name: str, email: str):
    """
    Create an ITP template based on the source tree of a Debian package.
    """
    env = Environment(
        loader=PackageLoader("debutils"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("itp.jinja")

    try:
        with click.open_file("debian/control", "r") as f:
            control = Deb822(f)
            package = control["Source"]
            section = control["Section"]
            url = control["Homepage"]
            short_desc, long_desc = next(Deb822.iter_paragraphs(f))["Description"].split(
                "\n", 1
            )
    except FileNotFoundError:
        package = "TODO"
        section = "TODO"
        url = "TODO"
        short_desc = "TODO"
        long_desc = "TODO (package long description)"

    try:
        with click.open_file("debian/copyright", "r") as f:
            copyr = Copyright(f)
            upstream = copyr.header.upstream_contact
            paragraph = copyr.find_files_paragraph(".")
            if paragraph is None:
                lic = "TODO"
            else:
                lic = paragraph.license._asdict()["synopsis"]
                if lic is None or lic == "":
                    lic = "TODO"
    except FileNotFoundError:
        upstream = ["TODO"]
        lic = "TODO"

    try:
        with click.open_file("debian/changelog", "r") as f:
            changelog = Changelog(f)
            deb_rev = r"\-.*$"
            deb_ext = r"[\+~](debian|dfsg|ds|deb)(\.)?(\d+)?$"
            version = str(changelog.version)
            version = re.sub(deb_rev, "", version)
            version = re.sub(deb_ext, "", version)
    except FileNotFoundError:
        version = "TODO"

    lang = fetch_lang(section)

    cc = fetch_cc(lang)

    message = template.render(
        name=name,
        email=email,
        cc=cc,
        package=package,
        license=lic,
        upstream=upstream,
        version=version,
        url=url,
        lang=lang,
        short_desc=short_desc,
        long_desc=long_desc,
    )

    output.write(message.encode())


def fetch_lang(section: str):
    if section == "golang" or Path("go.mod").exists():
        return "Go"
    if section == "python" or Path("pyproject.toml").exists() or Path("requirements.txt").exists():
        return "Python"
    if section == "javascript" or Path("package.json").exists():
        return "JavaScript"
    return "TODO"


def fetch_cc(lang: str):
    cc = ["debian-devel@lists.debian.org"]
    if lang == "Go":
        cc.append("debian-go@lists.debian.org")
    return cc
