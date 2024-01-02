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

from typing import List, Union

import click
from treelib import Tree

from debutils.go.session import GoExecutionError, GoSession
from debutils.go.packages import DebianGolangPackages
from debutils.go.vcs import import_path_root_repo


@click.command()
@click.argument("import-path")
@click.option(
    "--show-packaged-deps",
    is_flag=True,
    default=False,
    help="Shows packaged dependencies in output as well.",
)
@click.option(
    "--ignore-packaged",
    is_flag=True,
    default=False,
    help="Ignore whether the given import path is already packaged in Debian.",
)
@click.option(
    "--tree/--no-tree",
    "use_tree",
    default=True,
    help="Output a pretty tree instead of using indents.",
)
@click.option(
    "--recursive/--no-recursive",
    default=True,
    help="Recursively check dependencies. Disabling is useful if you"
    "want a quick check of direct dependencies only.",
)
@click.option(
    "--test-deps/--no-test-deps",
    default=False,
    help="Include test dependencies in the estimate.",
)
def estimate(
    import_path,
    show_packaged_deps,
    ignore_packaged,
    use_tree,
    recursive,
    test_deps,
):
    """
    Estimate work required to package a given Go module.

    High internet usage, so be careful when using this on a metered connection.
    """

    package, _ = import_path_root_repo(import_path)

    with GoSession() as session:
        deb_packages = DebianGolangPackages()

        if deb_package := deb_packages.is_packaged(package):
            click.secho(f"Already packaged in Debian: {deb_package}", fg="yellow")
            click.echo(f"https://tracker.debian.org/{deb_package}")
            if not ignore_packaged:
                return

        seen = []
        errors = []

        if use_tree:
            tree = Tree()
            tree.create_node(package, package)
            dependency_tree(
                session,
                seen,
                errors,
                package,
                show_packaged_deps,
                deb_packages,
                1,
                recursive,
                tree,
            )
            click.echo(tree.show(stdout=False))
        else:
            click.echo(package)
            dependency_tree(
                session,
                seen,
                errors,
                package,
                show_packaged_deps,
                deb_packages,
                1,
                recursive,
            )

        for error in errors:
            click.echo(error)


def dependency_tree(
    session: GoSession,
    seen: List[str],
    errors: List[GoExecutionError],
    package: str,
    show_packaged_deps: bool,
    debian_packages: DebianGolangPackages,
    level: int,
    recursive: bool,
    tree: Union[Tree, None] = None,
):
    try:
        dep_packages = session.get_package_dependencies(package)
    except GoExecutionError as error:
        errors.append(error)
        if tree is None:
            click.secho(f"{'  ' * level}Error getting dependencies", fg="red")
        else:
            tree.create_node(
                click.style("Error getting dependencies", fg="red"),
                f"{package}_error",
                parent=package,
            )
        return
    for dep_package, _ in dep_packages:
        if debian_package := debian_packages.library_is_packaged(dep_package):
            if show_packaged_deps:
                if tree is None:
                    click.secho(
                        f"{'  ' * level}{dep_package} ({debian_package})",
                        fg="green",
                    )
                else:
                    tree.create_node(
                        click.style(
                            f"{dep_package} ({debian_package})",
                            fg="green",
                        ),
                        f"{package}_{dep_package}",
                        parent=package,
                    )
        elif dep_package in seen:
            if tree is None:
                click.secho(f"{'  ' * level}{dep_package} (seen)", fg="blue")
            else:
                tree.create_node(
                    click.style(f"{dep_package} (seen)", fg="blue"),
                    f"{package}_{dep_package}",
                    parent=package,
                )
        else:
            if tree is None:
                click.echo(f"{'  ' * level}{dep_package}")
            else:
                tree.create_node(
                    dep_package,
                    dep_package,
                    parent=package,
                )
            seen.append(dep_package)
            if recursive:
                dependency_tree(
                    session,
                    seen,
                    errors,
                    dep_package,
                    show_packaged_deps,
                    debian_packages,
                    level + 1,
                    recursive,
                    tree,
                )
