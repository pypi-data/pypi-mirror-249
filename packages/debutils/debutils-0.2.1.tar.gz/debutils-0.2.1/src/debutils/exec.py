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

from typing import Callable, List

import click


def exec_exists(name: str) -> bool:
    from shutil import which

    return which(name) is not None


def need_exec(execs: List[str]):
    def _need_exec(func: Callable):
        def command(*args, **kwargs):
            missing = False
            for exec in execs:
                if not exec_exists(exec):
                    click.secho(
                        f"The '{exec}' executable is not available on your system, but this command requires it.",
                        fg="red",
                    )
                    missing = True
            if missing:
                return
            else:
                func(*args, **kwargs)

        command.__doc__ = func.__doc__
        command.__name__ = func.__name__
        return command

    return _need_exec
