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

import re
from typing import Tuple, Union

import requests

GO_IMPORT_META_REGEX = re.compile(
    r"<meta\s+name=\"?go-import\"?\s*content=\"(\S*) git (\S*)\"\s*/?>"
)


def import_path_root_repo(path: str) -> Tuple[str, str]:
    if path.split("/")[0] == "github.com":
        repo = "/".join(path.split("/")[0:3])
        return (repo, "https://" + repo)
    try:
        return get_repo_meta(path)
    except NoRootRepoError:
        raise NoRootRepoError(path)


def get_repo_meta(path: str) -> Tuple[str, str]:
    res = requests.get("https://" + path + "?go-get=1", timeout=60)
    match = GO_IMPORT_META_REGEX.search(res.text)
    if match is None:
        parts = path.split("/")
        if len(parts[:-1]) < 1:
            raise NoRootRepoError
        else:
            return get_repo_meta("/".join(parts[:-1]))
    return (
        match.group(1),
        "https://"
        + (match.group(2)[:-4] if match.group(2).endswith(".git") else match.group(2)),
    )


class NoRootRepoError(Exception):
    def __init__(self, path: Union[str, None] = None):
        if path is not None:
            super().__init__(f"No root repo could be determined for the path '{path}'")
        else:
            super().__init__(f"No root repo could be determined")
