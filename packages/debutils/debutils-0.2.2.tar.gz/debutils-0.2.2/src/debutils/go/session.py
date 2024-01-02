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

import os.path
import re
import subprocess
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory
from typing import List, Tuple

from debutils.go.vcs import import_path_root_repo

# Definitions:
# package = Go package (repo root with go.mod)
# deb_package = Debian package
# module = Go subpackage (subdirs within package)
# import_path = import path of Go package or Go module


class GoSession:
    def __init__(self):
        self.tempdir = TemporaryDirectory()
        self.gopath = Path(self.tempdir.name)

    downloaded_modules = []

    def cleanup(self):
        self.tempdir.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()

    def get_stdlib(self):
        out = subprocess.run(
            ["env", "GO111MODULE=off", f"GOPATH={self.gopath}", "go", "list", "std"],
            capture_output=True,
        )
        if out.returncode != 0:
            raise GoExecutionError(out.returncode, out.args)
        return [*out.stdout.decode().splitlines(), "C"]

    def get_package_modules(self, package):
        if not (self.gopath / "src" / package).exists():
            self.go_get(package)

        out = subprocess.run(
            ["env", f"GOPATH={self.gopath}", "go", "list", f"{package}/..."],
            capture_output=True,
            cwd=self.gopath / "src" / package,
        )
        if out.returncode != 0:
            raise GoExecutionError(out.returncode, out.args)

        def decode_map(s):
            return s.decode()

        return list(map(decode_map, out.stdout.splitlines()))

    def get_package_main_modules(self, package):
        modules = self.get_package_modules(package)
        main_modules = []
        for module in modules:
            out = subprocess.run(
                [
                    "env",
                    f"GOPATH={self.gopath}",
                    "go",
                    "list",
                    "-f",
                    "{{.Name}}",
                    module,
                ],
                capture_output=True,
                cwd=self.gopath / "src" / package,
            )
            if out.returncode != 0:
                raise GoExecutionError(out.returncode, out.args)
            if out.stdout.decode().strip() == "main":
                main_modules.append(module)
        return main_modules

    def get_package_dependencies(self, package: str, test=False) -> List[Tuple[str, str]]:
        self.go_get(package)
        stdlib = self.get_stdlib()
        all_deps = []
        out = subprocess.run(
            [
                "env",
                f"GOPATH={self.gopath}",
                "GO111MODULE=off",
                "go",
                "list",
                "-f",
                "{{.TestImports}}" if test else "{{.Imports}}",
                f"{package}/...",
            ],
            cwd=(self.gopath / "src" / package),
            capture_output=True,
        )
        if out.returncode != 0:
            raise GoExecutionError(out.returncode, out.args)
        for pkg in out.stdout.splitlines():
            dep_string = pkg.strip().decode()[1:-1]
            all_deps += dep_string.split(" ")

        def filter_deps(dep: str):
            return not dep.startswith(package) and dep not in stdlib and dep != ""

        deps = remove_duplicates(list(filter(filter_deps, all_deps)))

        def import_path_root_map(import_path):
            return import_path_root_repo(import_path)

        return remove_duplicates(list(map(import_path_root_map, deps)))

    def check_for_go_files(self, import_path):
        # instead of using go get and checking for an error, we'll check manually in GOPATH
        files = list((self.gopath / "src" / import_path).glob("*.go"))
        return len(files) > 0

    def strip_tag_suffix(self, import_path):
        return re.sub(r"/v\d+$", "", import_path)

    def go_get(self, package):
        self.go_get_module(package + '/...')

    def go_get_module(self, import_path):
        if import_path in self.downloaded_modules:
            return
        out = subprocess.run(
            [
                "env",
                "GO111MODULE=off",
                f"GOPATH={self.gopath}",
                "go",
                "get",
                import_path,
            ],
            check=False,
        )
        if out.returncode != 0:
            if out.stderr is not None and "no Go files" in out.stderr.decode():
                raise NoGoFilesError(import_path)
            else:
                raise GoExecutionError(out.returncode, out.args)
        vendor_dirs = list((self.gopath / "src").glob("**/vendor"))
        if len(vendor_dirs) > 0:
            for dir in vendor_dirs:
                rmtree(dir)
            out = subprocess.run(
                [
                    "env",
                    "GO111MODULE=off",
                    f"GOPATH={self.gopath}",
                    "go",
                    "get",
                    import_path,
                ],
            )
            if out.returncode != 0:
                raise GoExecutionError(out.returncode, out.args)


class NoGoFilesError(Exception):
    def __init__(self, path: str):
        super().__init__(f"No Go files were found in {path}")


def remove_duplicates(l):
    return list(dict.fromkeys(l))

class GoExecutionError(subprocess.CalledProcessError):
    pass
