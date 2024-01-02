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

from typing import Union
import requests
from urllib.parse import urlparse


def get_short_desc(repo_url: str) -> Union[str, None]:
    url = urlparse(repo_url)
    desc = None

    if url.hostname == "github.com":
        repo = requests.get(
            "https://api.github.com/repos" + url.path, timeout=60
        ).json()
        if len(repo["description"]) > 0:
            desc = repo["description"]

    if desc is None:
        return None

    desc = remove_punctuation(desc)
    desc = remove_article(desc)
    desc = lower_first_letter(desc)
    return desc


def remove_punctuation(s: str) -> str:
    if s[-1] in [".", "!", "?"]:
        return s[:-1]
    else:
        return s


def remove_article(s: str) -> str:
    if s.lower().startswith("a "):
        return s[2:]
    elif s.lower().startswith("an "):
        return s[3:]
    else:
        return s

def lower_first_letter(s: str) -> str:
    return s[0].lower() + s[1:]
