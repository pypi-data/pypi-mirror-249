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

from enum import Enum, auto
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from datetime import datetime
import tarfile
from shutil import rmtree
from typing import Dict, List, Tuple, Union
from urllib.parse import urlparse
import click
from jinja2 import Environment, PackageLoader, select_autoescape
import questionary
from infer_license.api import guess_file
from packaging.version import Version

from debutils.exec import need_exec
from debutils.go.debian import debian_source_name_from_go_package, short_host
from debutils.go.session import GoExecutionError, GoSession
from debutils.go.packages import DebianGolangPackages
from debutils.go.vcs import NoRootRepoError, import_path_root_repo
from debutils.licenses import KNOWN_LICENSES, get_license_text
from debutils.repos.desc import get_short_desc
from debutils.salsa import salsa_repo_exists
from debutils.wnpp import get_itp, get_rfp


@click.command()
@click.argument("import-path")
@click.option(
    "--type",
    "package_type_opt",
    required=False,
    type=click.Choice(["l", "l+b", "b+l", "b"], case_sensitive=False),
    help="Type of software being packaged.",
)
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
@click.option(
    "--ignore-packaged",
    is_flag=True,
    default=False,
    help="Ignore whether the given import path is already packaged in Debian.",
)
@click.option(
    "--ignore-salsa",
    is_flag=True,
    default=False,
    help="Ignore whether the package already has a Salsa repo.",
)
@need_exec(["git", "gbp"])
def make(import_path, package_type_opt, name, email, ignore_packaged, ignore_salsa):
    """
    Prepare a Go module for packaging in Debian.
    """
    with MakeGoSession() as session:
        try:
            go_package, git_repo = import_path_root_repo(import_path)
        except NoRootRepoError as error:
            click.echo(error)
            click.secho("Did you specify a Go package import path?", fg="yellow")
            return
        if go_package != import_path:
            click.echo(
                f"Continuing with repo root {go_package} instead of {import_path}"
            )

        debian_packages = DebianGolangPackages()

        if deb_package := debian_packages.is_packaged(go_package):
            click.secho(f"Already packaged in Debian: {deb_package}", fg="yellow")
            click.echo(f"https://tracker.debian.org/{deb_package}")
            if not ignore_packaged:
                click.secho(
                    "Pass --ignore-packaged to ignore this warning and continue.",
                    fg="cyan",
                )
                return

        debian_source_package = debian_source_name_from_go_package(go_package, True)

        debian_library_package = debian_source_package + "-dev"

        all_binaries: List[str] = session.get_package_main_modules(go_package)

        if len(all_binaries) > 0:
            click.echo("Found binaries:")
            for binary in all_binaries:
                click.echo(f" - {binary.split('/')[-1]} ({binary})")

        if salsa_repo_exists("go-team/packages/" + debian_source_package):
            click.secho(f"Salsa repo already exists for this package", fg="yellow")
            click.echo(
                f"https://salsa.debian.org/go-team/packages/{debian_source_package}"
            )
            if not ignore_salsa:
                click.secho(
                    "Pass --ignore-salsa to ignore this warning and continue.",
                    fg="cyan",
                )
                return

        wnpp = None

        click.secho(f"Checking for wnpp bug for: {debian_source_package}", fg="blue")
        if itp := get_itp(debian_source_package):
            wnpp = itp[0]
            click.secho(f"[#{itp[0]}] ITP: {itp[1]} -- {itp[2]}", fg="cyan")
        elif rfp := get_rfp(debian_source_package):
            wnpp = rfp[0]
            click.secho(f"[#{rfp[0]}] RFP: {rfp[1]} -- {rfp[2]}", fg="cyan")

        binary_word = "binaries" if len(all_binaries) > 1 else "binary"

        if package_type_opt is not None:
            package_type: PackageType = PackageType.from_opt(package_type_opt)
        elif len(all_binaries) == 0:
            package_type: PackageType = PackageType.LIBRARY
        else:
            package_type: PackageType = questionary.select(
                "What type of software are you packaging?",
                choices=[
                    questionary.Choice(
                        "Library only", value=PackageType.LIBRARY, checked=True
                    ),
                    questionary.Choice(
                        f"Library and accompanying {binary_word}",
                        value=PackageType.LIBRARY_AND_BINARY,
                    ),
                    questionary.Choice(
                        f"{binary_word.capitalize()} and accompanying library",
                        value=PackageType.BINARY_AND_LIBRARY,
                    ),
                    questionary.Choice(
                        f"{binary_word.capitalize()} only", value=PackageType.BINARY
                    ),
                ],
            ).ask()

        selected_binaries: List[str] = []

        if package_type.has_binary():
            if len(all_binaries) > 1:

                def binary_choice_map(binary: str):
                    return questionary.Choice(
                        f"{binary.split('/')[-1]} ({binary})", value=binary
                    )

                choices = list(map(binary_choice_map, all_binaries))
                selected_binaries = questionary.checkbox(
                    "Which binaries would you like to include?", choices=choices
                ).ask()
            else:
                selected_binaries = all_binaries

            wnpp_bugs = []
            for binary in selected_binaries:
                short_name = binary.split("/")[-1]
                if salsa_repo_exists("go-team/packages/" + short_name):
                    click.secho(
                        f"Salsa repo of the same name exists for the '{short_name}' binary",
                        fg="yellow",
                    )
                    click.echo(
                        f"https://salsa.debian.org/go-team/packages/{short_name}"
                    )

                click.secho(f"Checking for wnpp bug for: {short_name}", fg="blue")
                if itp := get_itp(short_name):
                    wnpp_bugs.append(itp[0])
                    click.secho(f"[#{itp[0]}] ITP: {itp[1]} -- {itp[2]}", fg="cyan")
                elif rfp := get_rfp(short_name):
                    wnpp_bugs.append(rfp[0])
                    click.secho(f"[#{rfp[0]}] RFP: {rfp[1]} -- {rfp[2]}", fg="cyan")
            if wnpp is None and len(wnpp_bugs) == 1:
                wnpp = wnpp_bugs[0]

        if (
            package_type == PackageType.BINARY_AND_LIBRARY
            or package_type == PackageType.BINARY
        ):

            def binary_choice_map(binary: str):
                return questionary.Choice(
                    f"{binary.split('/')[-1]} ({binary})", value=binary.split("/")[-1]
                )

            choices = list(map(binary_choice_map, selected_binaries))
            choices.insert(
                0,
                questionary.Choice(
                    debian_source_package, value=debian_source_package, checked=True
                ),
            )

            debian_source_package = questionary.select(
                "What do you want to name the source package?", choices=choices
            ).ask()

        work_dir = Path(debian_source_package)

        if work_dir.exists():
            click.secho(
                f"Output directory '{work_dir}' already exists",
                fg="red",
            )
            return

        work_dir.mkdir()

        version, versioned, repack, tarball = session.prepare_upstream(
            debian_source_package, git_repo
        )

        out = subprocess.run(["git", "init", "-b", "debian/sid"], cwd=work_dir)
        if out.returncode != 0:
            raise GitExecutionError(out.returncode, out.args)

        out = subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "git@salsa.debian.org:go-team/packages/"
                + debian_source_package
                + ".git",
            ],
            cwd=work_dir,
        )
        if out.returncode != 0:
            raise GitExecutionError(out.returncode, out.args)

        out = subprocess.run(
            [
                "gbp",
                "import-orig",
                "--no-interactive",
                "--debian-branch=debian/sid",
                os.path.join("..", tarball),
            ],
            cwd=work_dir,
        )
        if out.returncode != 0:
            raise GbpExecutionError(out.returncode, out.args)

        with open(work_dir / ".gitignore", "a") as file:
            file.write("\n/.pc/\n/_build/")
        out = subprocess.run(["git", "add", ".gitignore"], cwd=work_dir)
        if out.returncode != 0:
            raise GitExecutionError(out.returncode, out.args)
        out = subprocess.run(
            ["git", "commit", "-m", "Add quilt and build directories to gitignore"],
            cwd=work_dir,
        )
        if out.returncode != 0:
            raise GitExecutionError(out.returncode, out.args)

        debian_deps = []
        debian_build_deps = ["debhelper-compat (= 13)", "dh-golang", "golang-any"]

        try:
            go_deps = session.get_package_dependencies(go_package)
            for dep, _ in go_deps:
                if debian_package := debian_packages.library_is_packaged(dep):
                    debian_deps.append(debian_package)
                else:
                    click.secho(
                        f"Dependency {dep} is not packaged in Debian!", fg="yellow"
                    )

            debian_build_deps += debian_deps

            go_test_deps = session.get_package_dependencies(go_package, True)
            for dep, _ in go_test_deps:
                if dep in go_deps:
                    continue
                elif (
                    debian_package := debian_packages.library_is_packaged(dep)
                ) and debian_package not in debian_deps:
                    debian_build_deps.append(debian_package + " <!nocheck>")
                else:
                    click.secho(
                        f"Test dependency {dep} is not packaged in Debian!", fg="yellow"
                    )
        except Exception as e:
            click.echo(e)
            click.secho(
                "An error occurred fetching dependencies, skipping...", fg="red"
            )

        short_desc = get_short_desc(git_repo)

        (work_dir / "debian").mkdir()

        env = Environment(
            loader=PackageLoader("debutils"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        header_template = env.get_template("go/control/header.jinja")

        control_stanzas = []

        control_stanzas.append(
            header_template.render(
                source=debian_source_package,
                uploaders=[f"{name} <{email}>"],
                lib_deps=debian_build_deps,
                homepage=git_repo,
                go_import_path=import_path,
            )
        )

        match package_type:
            case PackageType.LIBRARY:
                control_stanzas.append(
                    render_library_package(
                        env, debian_library_package, short_desc, debian_deps
                    )
                )
            case PackageType.BINARY:
                for binary in selected_binaries:
                    control_stanzas.append(
                        render_binary_package(env, binary.split("/")[-1], short_desc)
                    )
            case PackageType.LIBRARY_AND_BINARY:
                control_stanzas.append(
                    render_library_package(
                        env, debian_library_package, short_desc, debian_deps
                    )
                )
                for binary in selected_binaries:
                    control_stanzas.append(
                        render_binary_package(env, binary.split("/")[-1], short_desc)
                    )
            case PackageType.BINARY_AND_LIBRARY:
                for binary in selected_binaries:
                    control_stanzas.append(
                        render_binary_package(env, binary.split("/")[-1], short_desc)
                    )
                control_stanzas.append(
                    render_library_package(
                        env, debian_library_package, short_desc, debian_deps
                    )
                )

        control = "\n\n".join(control_stanzas)

        with (work_dir / "debian/control").open("x") as file:
            file.write(control)

        lic = "TODO"

        for file in work_dir.glob("*"):
            if (
                file.name.lower()
                in ["license", "license.md", "copying", "copying.md", "unlicense"]
                and (guess := guess_file(str(file)))
                and guess.shortname in KNOWN_LICENSES
            ):
                lic = KNOWN_LICENSES[guess.shortname]
                break

        copyr_template = env.get_template("go/copyright.jinja")

        with (work_dir / "debian/copyright").open("x") as file:
            file.write(
                copyr_template.render(
                    license=lic,
                    license_text=get_license_text(lic),
                    year=datetime.now().strftime("%Y"),
                    name=name,
                    email=email,
                    homepage=git_repo,
                    upstream_name=go_package.split("/")[-1],
                    repack=repack,
                )
            )

        changelog_template = env.get_template("go/changelog.jinja")

        with (work_dir / "debian/changelog").open("x") as file:
            file.write(
                changelog_template.render(
                    source=debian_source_package,
                    debian_version=version + "-1",
                    itp=wnpp if wnpp is not None else "TODO",
                    name=name,
                    email=email,
                    date=datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
                    + " "
                    + datetime.utcnow().astimezone().strftime("%z")[:5],
                )
            )

        with (work_dir / "debian/.gitignore").open("x") as file:
            file.write(
                "*.debhelper\n"
                "*.log\n"
                "*.substvars\n"
                "/.debhelper/\n"
                "/debhelper-build-stamp/\n"
                "/files\n"
            )
            if package_type.has_binary():
                for binary in selected_binaries:
                    file.write("/" + binary.split("/")[-1] + "/\n")
            if package_type.has_library():
                file.write("/" + debian_library_package + "/\n")

        with (work_dir / "debian/rules").open("x") as file:
            file.write(
                "#!/usr/bin/make -f\n"
                "\n"
                "%:\n"
                "\tdh $@ --builddirectory=_build --buildsystem=golang\n"
            )
            if package_type == PackageType.BINARY:
                file.write(
                    "\n"
                    "override_dh_auto_install:\n"
                    "\tdh_auto_install -- --no-source\n"
                )

        (work_dir / "debian/rules").chmod(0o0755)

        (work_dir / "debian/source").mkdir()

        with (work_dir / "debian/source/format").open("x") as file:
            file.write("3.0 (quilt)\n")

        with (work_dir / "debian/gbp.conf").open("x") as file:
            file.write("[DEFAULT]\n" "debian-branch = debian/sid\n" "dist = DEP14\n")

        if (
            package_type == PackageType.BINARY_AND_LIBRARY
            or package_type == PackageType.LIBRARY_AND_BINARY
        ):
            with (work_dir / f"debian/{debian_library_package}.install").open(
                "x"
            ) as file:
                file.write("usr/share\n")
            if len(selected_binaries) > 1:
                for binary in selected_binaries:
                    with (work_dir / f"debian/{binary.split('/')[-1]}.install").open(
                        "x"
                    ) as file:
                        file.write(f"usr/bin/{binary.split('/')[-1]}\n")
            else:
                with (
                    work_dir / f"debian/{selected_binaries[0].split('/')[-1]}.install"
                ).open("x") as file:
                    file.write("usr/bin\n")

        with (work_dir / "debian/watch").open("x") as file:
            file.write(gen_debian_watch(env, git_repo, versioned, repack))

        (work_dir / "debian/upstream").mkdir()

        with (work_dir / "debian/upstream/metadata").open("x") as file:
            file.write(gen_debian_upstream_metadata(git_repo))

        with (work_dir / "debian/gitlab-ci.yml").open("x") as file:
            file.write(
                """# auto-generated, DO NOT MODIFY.
# The authoritative copy of this file lives at:
# https://salsa.debian.org/go-team/infra/pkg-go-tools/blob/master/config/gitlabciyml.go
---
include:
  - https://salsa.debian.org/go-team/infra/pkg-go-tools/-/raw/master/pipeline/test-archive.yml
"""
            )

        click.secho(
            "Packaging prepared successfully in " + str(work_dir), bold=True, fg="green"
        )
        click.echo("")
        click.echo("Resolve all the TODOs in debian/, find them using:")
        click.echo("    grep -r TODO debian/")
        click.echo("")
        click.echo("To build the package, its recommended to use sbuild:")
        click.echo("    sbuild")
        click.echo("See https://wiki.debian.org/sbuild#Setup for setup instructions.")
        click.echo("")
        click.echo("When you finish packaging, commit your changes:")
        click.echo("    git add debian && git commit -S -m 'Initial packaging'")
        click.echo("")
        click.echo("To create the packaging repo on Salsa, use:")
        click.echo("    dh-make-golang create-salsa-project " + debian_source_package)
        click.echo("")
        click.echo("Once you are happy with your work, push to Salsa:")
        click.echo("    git push --all && git push --tags")
        click.echo("    # or")
        click.echo("    gbp push")
        click.echo("")

        click.secho("debutils is experimental software!", bold=True, fg="yellow")
        click.secho("Please report any problems to", fg="yellow")
        click.secho("https://codeberg.org/Maytha8/debutils/issues", fg="yellow")


def gen_debian_watch(env: Environment, repo: str, versioned: bool, repack: bool) -> str:
    url = urlparse(repo)
    if versioned:
        if url.hostname == "github.com":
            template = env.get_template("go/watch/github.jinja")
            return template.render(repo=repo, repack=repack)
        template = env.get_template("go/watch/git_tags.jinja")
        return template.render(repo=repo, repack=repack)
    else:
        template = env.get_template("go/watch/git_commits.jinja")
        return template.render(repo=repo, repack=repack)


def gen_debian_upstream_metadata(repo: str) -> str:
    url = urlparse(repo)
    if url.hostname == "github.com":
        return (
            "---\n"
            "Bug-Database: " + repo + "/issues\n"
            "Bug-Submit: " + repo + "/issues/new\n"
            "Repository: " + repo + ".git\n"
            "Repository-Browse: " + repo + "\n"
        )
    return (
        "---\n"
        "Bug-Database: TODO\n"
        "Bug-Submit: TODO\n"
        "Repository: " + repo + ".git\n"
        "Repository-Browse: " + repo + "\n"
    )


def render_library_package(
    env: Environment, package: str, short_desc: Union[str, None], lib_deps: List[str]
):
    library_template = env.get_template("go/control/go_library.jinja")
    return library_template.render(
        package=package,
        lib_deps=lib_deps,
        short_desc=short_desc,
    )


def render_binary_package(env: Environment, package: str, short_desc: Union[str, None]):
    binary_template = env.get_template("go/control/go_binary.jinja")
    return binary_template.render(
        package=package,
        short_desc=short_desc,
    )


class PackageType(Enum):
    LIBRARY = auto()
    BINARY = auto()
    LIBRARY_AND_BINARY = auto()
    BINARY_AND_LIBRARY = auto()

    @classmethod
    def from_opt(cls, opt: str):
        match opt:
            case "l":
                return cls.LIBRARY
            case "b":
                return cls.BINARY
            case "l+b":
                return cls.LIBRARY_AND_BINARY
            case "b+l":
                return cls.BINARY_AND_LIBRARY
            case _:
                return cls.LIBRARY

    def has_library(self):
        return (
            self == self.__class__.LIBRARY
            or self == self.__class__.LIBRARY_AND_BINARY
            or self == self.__class__.BINARY_AND_LIBRARY
        )

    def has_binary(self):
        return (
            self == self.__class__.BINARY
            or self == self.__class__.LIBRARY_AND_BINARY
            or self == self.__class__.BINARY_AND_LIBRARY
        )


class MakeGoSession(GoSession):
    def prepare_upstream(self, source_package, git_repo):
        with TemporaryDirectory() as t:
            temp = Path(t)
            repo_path = temp / "repo"

            out = subprocess.run(["git", "clone", "--quiet", git_repo, repo_path])
            if out.returncode != 0:
                raise GitExecutionError(out.returncode, out.args)

            out = subprocess.run(
                ["git", "tag", "--list"], cwd=repo_path, capture_output=True
            )
            if out.returncode != 0:
                raise GitExecutionError(out.returncode, out.args)

            tags: Dict[Version, str] = {}
            all_tags = out.stdout.strip().decode()
            matches = re.findall(r"^(v?(\d[\d\.]+))$", all_tags, re.MULTILINE)
            for match in matches:
                tags[Version(match[1])] = match[0]

            versions = list(tags.keys())
            versions.sort()

            if len(versions) > 0:
                version: Tuple[str, str] = (str(versions[-1]), tags[versions[-1]])
                versioned = True
            else:
                out = subprocess.run(
                    ["git", "log", "-1", "--format=%cI %H"],
                    cwd=repo_path,
                    capture_output=True,
                )
                if out.returncode != 0:
                    raise GitExecutionError(out.returncode, out.args)

                [iso_date, hash] = out.stdout.strip().decode().split(" ")
                date = datetime.fromisoformat(iso_date).strftime("%Y%m%d")
                version: Tuple[str, str] = (f"0.0~git{date}.{hash[:7]}", hash)
                versioned = False

            out = subprocess.run(
                ["git", "checkout", "--quiet", version[1]],
                cwd=repo_path,
            )
            if out.returncode != 0:
                raise GitExecutionError(out.returncode, out.args)

            rmtree(repo_path / ".git")

            repack = False

            if (repo_path / "vendor").exists():
                version = (version[0] + "+ds", version[1])
                repack = True
                rmtree(repo_path / "vendor")

            if (repo_path / "debian").exists():
                rmtree(repo_path / "debian")

            tarball_path = Path(f"{source_package}_{version[0]}.orig.tar.xz")

            with tarfile.open(name=tarball_path, mode="x:xz") as tarball:
                tarball.add(repo_path, arcname=source_package)

            return (version[0], versioned, repack, tarball_path)


class InvalidInputError(Exception):
    def __init__(self):
        super().__init__("Invalid input recieved.")


class GitExecutionError(subprocess.CalledProcessError):
    pass


class GbpExecutionError(subprocess.CalledProcessError):
    pass
